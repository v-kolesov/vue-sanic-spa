import os
from sanic.response import json

import application

app = application.create('api')

@app.route("/")
async def test(request):
    return json({"hello": "world!"})

if __name__ == "__main__":                
    debug_mode =  os.getenv('API_MODE', '') == 'dev'   

    app.run(
        host='0.0.0.0',
        port=8000,
        debug=debug_mode, 
        access_log=debug_mode
    )
