import re
from flask import Flask, Response, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

def generate_ts_content(source_url, headers):
    ts = requests.get(source_url, headers=headers, stream=True)
    for chunk in ts.iter_content(chunk_size=1024):
        if chunk:
            yield chunk

@app.route('/<m3u8>')
def index(m3u8):
    source = request.url.replace('__', '/')
    source = source.replace('https://seashell-app-cdk6o.ondigitalocean.app/', '')
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

    return Response(generate_ts_content(source, headers), content_type='video/mp2t')

@app.route('/getm3u8', methods=['GET'])
def getm3u8():
    source = request.url.replace('https://seashell-app-cdk6o.ondigitalocean.app/getm3u8?source=', '')
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

    return Response(generate_ts_content(source, headers), content_type='video/mp2t')

@app.route('/getstream', methods=['GET'])
def getstream():
    param = request.args.get("param")

    if param == "getts":
        source = request.url.replace('https://seashell-app-cdk6o.ondigitalocean.app/getstream?param=getts&source=', '')
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

        return Response(generate_ts_content(source, headers), content_type='video/mp2t')

    if param == "getm3u8":
        videoid = request.args.get("videoid")
        veriler = {"AppId": "3", "AppVer": "1025", "VpcVer": "1.0.11", "Language": "tr", "Token": "", "VideoId": videoid}
        r = requests.post("https://melbet-17181.top/cinema", json=veriler)

        if "FullscreenAllowed" in r.text:
            veri = re.findall('"URL":"(.*?)"', r.text)
            veri = veri[0].replace("\/", "__")
            veri = veri.replace('edge3', 'edge10')
            veri = veri.replace('edge100', 'edge10')
            veri = veri.replace('edge4', 'edge10')
            veri = veri.replace('edge2', 'edge10')
            veri = veri.replace('edge5', 'edge10')
            veri = veri.replace('edge1', 'edge10')
            veri = veri.replace('edge6', 'edge10')
            veri = veri.replace('edge7', 'edge10')
            veri = veri.replace(':43434', '')
            veri = veri.replace('edge100', 'edge10')

            if "m3u8" in veri:
                return "https://turbo-turabi.volestream--geldi-kizlarr.workers.dev/" + veri + '&videoid=' + videoid
        else:
            return "Veri yok"

if __name__ == '__main__':
    app.run()
