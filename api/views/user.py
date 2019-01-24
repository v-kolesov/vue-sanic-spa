import ujson
import uuid
from marshmallow.validate import Length
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from sanic.views import HTTPMethodView
from marshmallow import Schema, fields
from sanic.response import json

class UserSchema(Schema):
    id = fields.Integer(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=[Length(min=4)])


class Auth(HTTPMethodView):
    async def get(self, request):
        return json({"hello": "world"})

    async def post(self, request):
        res, errs = UserSchema(exclude=['id']).load(request.json)
        if errs:
            return json({"valid": False, "data": errs}, status=400)


        async with request.app.db.acquire() as conn:
            _user = await conn.fetchrow('''
            SELECT * FROM users WHERE email=$1
            ''', res['email'])

        if not (
                _user and
                pbkdf2_sha256.verify(res['password'], _user['password'])
        ):
            return json({
                "valid": False,
                "data": 'Wrong email or password'
            }, status=401)


        data = UserSchema(exclude=['password']).dump(_user).data

        token = uuid.uuid4().hex

        await request.app.redis.set(token, ujson.dumps(data))

        return json({"valid": True, "data": {"access_token": token}})
