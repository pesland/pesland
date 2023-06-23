import asyncio
import re
from aiohttp import ClientSession
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

async def fetch_data(session, url, headers):
    async with session.get(url, headers=headers) as response:
        if response.status == 200:
            return await response.read()
        else:
            return None


@app.route('/<m3u8>')
async def index(m3u8):
    m3u8 = request.url.replace('__', '/')
    source = m3u8.replace('https://erdoganladevam.herokuapp.com/', '')
    source = source.replace('%2F', '/')
    source = source.replace('%3F', '?')
    videoid = request.args.get("videoid")
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "tr-TR, tr;q=0.9",
        "origin": "https://www.maltinok.com",
        "referer": "https://www.maltinok.com/",
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }
    
    async with ClientSession() as session:
        ts = await fetch_data(session, source, headers)
        tsal = ts.replace(videoid + '_', 'https://neset-baba-sigara.keremihsanozer.workers.dev/getstream?param=getts&source=https://edge10.xmediaget.com/hls-live/' + videoid + '/1/' + videoid + '_')

        if "internal" in tsal:
            tsal = tsal.replace('internal', 'https://neset-baba-sigara.keremihsanozer.workers.dev/getstream?param=getts&source=https://edge10.xmediaget.com/hls-live/' + videoid + '/1/internal')
        if "segment" in tsal:
            tsal = tsal.replace('\n' + 'media', '\n' + 'https://neset-baba-sigara.keremihsanozer.workers.dev/getstream?param=getts&source=https://edge10.xmediaget.com/hls-live/' + videoid + '/1/media')
        
        return tsal

@app.route('/getm3u8', methods=['GET'])
async def getm3u8():
    source = request.url.replace('https://erdoganladevam.herokuapp.com/getm3u8?source=', '')
    source = source.replace('%2F', '/')
    source = source.replace('%3F', '?')
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "tr-TR, tr;q=0.9",
        "origin": "https://www.maltinok.com",
        "referer": "https://www.maltinok.com/",
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }
    
    async with ClientSession() as session:
        ts = await fetch_data(session, source, headers)
        videoid = request.args.get("videoid")
        tsal = ts.replace(videoid + '_', 'https://erdoganladevam.herokuapp.com/getstream?param=getts&source=https://edge10.xmediaget.com/hls-live/' + videoid + '/1/' + videoid + '_')
        
        return tsal

@app.route('/getstream', methods=['GET'])
async def getstream():
    param = request.args.get("param")

    if param == "getts":
        source = request.url.replace('https://erdoganladevam.herokuapp.com/getstream?param=getts&source=', '')
        source = source.replace('%2F', '/')
        source = source.replace('%3F', '?')
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'tr-TR,tr;q=0.9',
            'origin': 'https://www.maltinok.com',
            'referer': 'https://www.maltinok.com/',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }

        async with aiohttp.ClientSession() as session:
            ts = await fetch_data(session, source, headers)
            if ts is not None:
                return ts
            else:
                return "Veri çekilemedi."
    elif param == "getm3u8":
        
        pass

if __name__ == '__main__':
    app.run()
