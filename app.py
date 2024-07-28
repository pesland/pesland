import requests
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import re
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Use a global session for making HTTP requests
session = requests.Session()

def fetch_url(url, headers):
    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None

def replace_patterns(text, videoid):
    text = text.replace(videoid + '_', f'https://googleuserproxy.global.ssl.fastly.net/getstream?param=getts&source=https://googleusercontent1x.global.ssl.fastly.net/hls-live/{videoid}/1/{videoid}_')
    text = text.replace('internal', f'https://googleuserproxy.global.ssl.fastly.net/getstream?param=getts&source=https://googleusercontent1x.global.ssl.fastly.net/hls-live/{videoid}/1/internal')
    text = text.replace('\n' + 'media', f'\nhttps://googleuserproxy.global.ssl.fastly.net/getstream?param=getts&source=https://googleusercontent1x.global.ssl.fastly.net/hls-live/{videoid}/1/media')
    return text

def add_cache_control(response):
    response.headers['Cache-Control'] = 'max-age=14400'
    return response

@app.route('/<m3u8>')
def index(m3u8):
    m3u8 = request.url.replace('__', '/')
    source = m3u8.replace('https://shark-app-oy2nm.ondigitalocean.app/', '').replace('%2F', '/').replace('%3F', '?')
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
    
    tsal = fetch_url(source, headers)
    if tsal:
        tsal = replace_patterns(tsal, videoid)
        response = Response(tsal)
        return add_cache_control(response)
    return add_cache_control(Response("Failed to fetch the URL", status=500))

@app.route('/getm3u8', methods=['GET'])
def getm3u8():
    source = request.url.replace('https://shark-app-oy2nm.ondigitalocean.app/getm3u8?source=', '').replace('%2F', '/').replace('%3F', '?')
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
    
    tsal = fetch_url(source, headers)
    videoid = request.args.get("videoid")
    if tsal:
        tsal = tsal.replace(videoid + '_', f'https://googleuserproxy.global.ssl.fastly.net/getstream?param=getts&source=https://edge10.xmediaget.com/hls-live/{videoid}/1/{videoid}_')
        response = Response(tsal)
        return add_cache_control(response)
    return add_cache_control(Response("Failed to fetch the URL", status=500))

@app.route('/getstream', methods=['GET'])
def getstream():
    param = request.args.get("param")

    if param == "getts":
        source = request.url.replace('https://shark-app-oy2nm.ondigitalocean.app/getstream?param=getts&source=', '').replace('%2F', '/').replace('%3F', '?')
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
        
        ts = fetch_url(source, headers)
        if ts:
            response = Response(ts, content_type='video/mp2t')
            return add_cache_control(response)
        return add_cache_control(Response("Failed to fetch the stream", status=500))
    
    if param == "getm3u8":
        videoid = request.args.get("videoid")
        veriler = {"AppId": "3", "AppVer": "1025", "VpcVer": "1.0.11", "Language": "tr", "Token": "", "VideoId": videoid}
        try:
            r = session.post("https://melbet-485485.top/cinema", json=veriler)
            r.raise_for_status()
            if "FullscreenAllowed" in r.text:
                veri = re.findall('"URL":"(.*?)"', r.text)[0].replace("\/", "__")
                veri = re.sub(r'edge[0-9]+', 'edge10', veri).replace(':43434', '')
                if "m3u8" in veri:
                    response = Response(f"https://shark-app-oy2nm.ondigitalocean.app/{veri}&videoid={videoid}")
                    return add_cache_control(response)
            return add_cache_control(Response("Veri yok"))
        except requests.RequestException as e:
            logging.error(f"Request failed: {e}")
            return add_cache_control(Response("Failed to fetch the URL", status=500))

if __name__ == '__main__':
    app.run()
