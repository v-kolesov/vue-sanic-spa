import os
import asyncpg
import asyncio_redis
from sanic import Sanic, Blueprint
from views import user
from migration import SCHEMA, LATEST_VERSION


def create(*args, **kwargs):
    app = Sanic(*args, **kwargs)
    before_server_start(app)
    after_server_stop(app)
    init_blueprints(app)
    return app


def before_server_start(app):
    @app.listener('before_server_start')
    async def run(app, loop):
        dsn='postgres://{user}:{pwd}@db/{database}'.format(
            user=os.getenv('POSTGRES_USER'),
            pwd=os.getenv('POSTGRES_PASSWORD'),
            database=os.getenv('POSTGRES_DB')
        )
        app.db = await asyncpg.create_pool(dsn, loop=loop, max_size=80)
        app.redis = await asyncio_redis.Pool.create(host='redis', poolsize=10)
        await db_migrate(app, SCHEMA, LATEST_VERSION)


def after_server_stop(app):
    @app.listener('after_server_stop')
    async def run(app, loop):
        await app.db.close()
        app.redis.close()

def init_blueprints(app):
    v1_0 = Blueprint('api', url_prefix='/v1.0')
    v1_0.add_route(user.Auth.as_view(), '/user/auth')
    app.blueprint(v1_0)


async def db_migrate(app, schema, version):
    async with app.db.acquire() as conn:
        result = await conn.fetchval(
            """
            select table_name from information_schema.tables
            where table_schema='public' and table_name = $1
            """, 'versions'
        )
        if result is None:
            num = 0
        else:
            num = await conn.fetchval("select id from versions limit 1")

        async with conn.transaction():
            while version > num:
                num += 1
                for sql in schema[num]['up']:
                    await conn.execute(*sql)

                await conn.execute('update versions set id=$1', num)

            while version < num:
                for sql in schema[num]['down']:
                    await conn.execute(*sql)
                num -= 1
                if num > 0:
                    await conn.execute('update versions set id=$1', num)
