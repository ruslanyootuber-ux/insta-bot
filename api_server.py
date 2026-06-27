from aiohttp import web

async def api_namoz_vaqtlari(request):
    data = {
        "mintaqa": "Yakkabog'",
        "vaqtlar": {"bomdod": "03:32", "peshin": "13:00", "asr": "17:45", "shom": "20:05", "xufton": "21:40"}
    }
    return web.json_response(data, headers={"Access-Control-Allow-Origin": "*"})

def get_app():
    app = web.Application()
    app.router.add_get('/api/namoz', api_namoz_vaqtlari)
    return app