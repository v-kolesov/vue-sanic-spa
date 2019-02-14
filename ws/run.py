
import os
from sanic import Sanic
import ujson
import asyncio_redis
from websockets.exceptions import ConnectionClosed

app = Sanic('websocket')


@app.listener('before_server_start')
async def start(app, loop):
    app.redis = await asyncio_redis.Pool.create(host='redis', poolsize=10)


@app.listener('after_server_stop')
async def stop(app, loop):    
    app.redis.close()


async def check_token(request):
    token = request.args['token']   
    
    
@app.websocket('/')
async def feed(request, ws):              
    while True:
        try:
            data = await ws.recv()
            if data:
                await ws.send(ujson.dumps(dict(status='ok', payload=data)))                            
              
        except  ConnectionClosed:
            print('Close')


if __name__ == "__main__":                
    debug_mode =  os.getenv('API_MODE', '') == 'dev'   

    app.run(
        host='0.0.0.0',
        port=8000,
        debug=debug_mode, 
        access_log=debug_mode
    )
