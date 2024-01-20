import requests
from flask import Flask, request
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

def fetch_data(url):
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
    ts = requests.get(url, headers=headers, stream=True)
    tsal = ""
    for chunk in ts.iter_content(chunk_size=128):
        tsal += chunk
    return tsal

def process_m3u8(source, videoid):
    tsal = fetch_data(source)
    tsal = tsal.replace(videoid+'_', 'https://seashell-app-cdk6o.ondigitalocean.app/getstream?param=getts&source=https://edge10.xmediaget.com/hls-live/'+videoid+'/1/'+videoid+'_')
    if "internal" in tsal:
        tsal = tsal.replace('internal', 'https://worker-holy-shadow-d82a.volestream--geldi-kizlarr.workers.dev/https://seashell-app-cdk6o.ondigitalocean.app/getstream?param=getts&source=https://edge10.xmediaget.com/hls-live/'+videoid+'/1/internal')
    if "segment" in tsal:
        tsal = tsal.replace('\n'+'media', '\n'+'https://worker-holy-shadow-d82a.volestream--geldi-kizlarr.workers.dev/https://seashell-app-cdk6o.ondigitalocean.app/getstream?param=getts&source=https://edge10.xmediaget.com/hls-live/'+videoid+'/1/media')
    return tsal

@app.route('/<m3u8>')
def index(m3u8):
    m3u8 = request.url.replace('__', '/')
    source = m3u8.replace('https://seashell-app-cdk6o.ondigitalocean.app/', '')
    source = source.replace('%2F', '/')
    source = source.replace('%3F', '?')
    videoid = request.args.get("videoid")
    return process_m3u8(source, videoid)

@app.route('/getm3u8', methods=['GET'])
def getm3u8():
    source = request.url.replace('https://seashell-app-cdk6o.ondigitalocean.app/getm3u8?source=', '')
    source = source.replace('%2F', '/')
    source = source.replace('%3F', '?')
    return fetch_data(source)

@app.route('/getstream', methods=['GET'])
def getstream():
    param = request.args.get("param")
    if param == "getts":
        source = request.url.replace('https://seashell-app-cdk6o.ondigitalocean.app/getstream?param=getts&source=', '')
        source = source.replace('%2F', '/')
        source = source.replace('%3F', '?')
        return fetch_data(source)
    elif param == "getm3u8":
        videoid = request.args.get("videoid")
        veriler = {"AppId": "3", "AppVer": "1025", "VpcVer": "1.0.11", "Language": "tr", "Token": "", "VideoId": videoid}
        r = requests.post("https://melbet-17181.top/cinema", json=veriler)
        if "FullscreenAllowed" in r.text:
            veri = r.text
            veri = re.findall('"URL":"(.*?)"', veri)
            veri = veri[0].replace("\/", "__")
            veri = veri.replace('edge3', 'edge10').replace('edge100', 'edge10').replace('edge4', 'edge10').replace('edge2', 'edge10').replace('edge5', 'edge10').replace('edge1', 'edge10').replace('edge6', 'edge10').replace('edge7', 'edge10').replace(':43434', '').replace('edge100', 'edge10')
            if "m3u8" in veri:
                return "https://seashell-app-cdk6o.ondigitalocean.app/" + veri + '&videoid=' + videoid
        else:
            return "Veri yok"

if __name__ == '__main__':
    app.run()
