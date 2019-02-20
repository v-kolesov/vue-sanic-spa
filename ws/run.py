
import os
from time import time
from sanic import Sanic
import ujson
import asyncio_redis
from websockets.exceptions import ConnectionClosed

app = Sanic('websocket')

conn = {}
CONN_CACHE_TIME = 10 # sec

@app.listener('before_server_start')
async def start(app, loop):
    app.redis = await asyncio_redis.Pool.create(host='redis', poolsize=10)


@app.listener('after_server_stop')
async def stop(app, loop):    
    app.redis.close()


async def check_token(request):
    token = request.args['token']   
    

async def checkTokenAlive(ws, token):
    if time() - conn.get(ws, 0) > CONN_CACHE_TIME:
        token_exists = await app.redis.exists(token)
        if token_exists:
            conn[ws]=time()            
        else:
            return False
    return True
    

@app.websocket('/')
async def feed(request, ws):                      
    token = request.args['token'].pop()
    if token:
        isAlive = await checkTokenAlive(ws, token)
        while isAlive:
            try:
                data = await ws.recv()            
                if data:                
                    if data=="/out":
                        await ws.close()
                    await ws.send(f'I\'ve received: {data}')                            
            except  ConnectionClosed:
                pass
            isAlive = await checkTokenAlive(ws, token)
    await ws.close()


if __name__ == "__main__":                
    debug_mode =  os.getenv('API_MODE', '') == 'dev'   

    app.run(
        host='0.0.0.0',
        port=8000,
        debug=debug_mode, 
        access_log=debug_mode
    )
