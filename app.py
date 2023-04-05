import re
import aiohttp
from aiohttp import web

app = web.Application()

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def replace_text(videoid, text):
    # Replace videoid+'_'
    pattern = re.compile(re.escape(videoid + '_'))
    text = pattern.sub(f'https://volestream.herokuapp.com/getstream?param=getts&source=https://edge10.xmediaget.com/hls-live/{videoid}/1/{videoid}_', text)

    # Replace internal
    pattern = re.compile(re.escape('internal'))
    text = pattern.sub(f'https://volestream.herokuapp.com/getstream?param=getts&source=https://edge10.xmediaget.com/hls-live/{videoid}/1/internal', text)

    # Replace segment
    pattern = re.compile(re.escape('\nmedia'))
    text = pattern.sub(f'\nhttps://volestream.herokuapp.com/getstream?param=getts&source=https://edge10.xmediaget.com/hls-live/{videoid}/1/media', text)

    return text

async def get_m3u8(request):
    source = request.query.get('source')
    source = source.replace('%2F', '/')
    source = source.replace('%3F', '?')

    async with aiohttp.ClientSession() as session:
        text = await fetch(session, source)
        videoid = request.query.get('videoid')
        text = await replace_text(videoid, text)

    return web.Response(text=text)

async def get_stream(request):
    param = request.query.get('param')
    if param == 'getts':
        source = request.query.get('source')
        source = source.replace('%2F','/')
        source = source.replace('%3F','?')

        async with aiohttp.ClientSession() as session:
            text = await fetch(session, source)

        return web.Response(text=text)
    else:
        return web.Response(text='Invalid parameter')

app.add_routes([
    web.get('/getm3u8', get_m3u8),
    web.get('/getstream', get_stream)
])

if __name__ == '__main__':
    web.run_app(app)
