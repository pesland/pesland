import requests
from flask import Flask, request, Response
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

# Global session for making HTTP requests
session = requests.Session()

# Helper function to decode URLs
def decode_url(url):
    return url.replace('%2F', '/').replace('%3F', '?').replace('%3A', ':').replace('%3D', '=').replace('%26', '&')

@app.route('/<path:m3u8>')
def index(m3u8):
    # Decode and reconstruct source URL
    source = decode_url(request.url.replace('__', '/').replace('https://lobster-app-bwfjt.ondigitalocean.app/', ''))
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
    
    response = session.get(source, headers=headers)
    content = response.text

    # Replace URLs in the content
    content = content.replace(videoid + '_', 'https://1xb.global.ssl.fastly.net/getstream?param=getts&source=https://edge10.xmediaget.com/hls-live/' + videoid + '/1/' + videoid + '_')
    content = content.replace('internal', 'https://1xb.global.ssl.fastly.net/getstream?param=getts&source=https://edge10.xmediaget.com/hls-live/' + videoid + '/1/internal')
    content = content.replace('\nmedia', '\nhttps://1xb.global.ssl.fastly.net/getstream?param=getts&source=https://edge10.xmediaget.com/hls-live/' + videoid + '/1/media')

    # Add cache headers to the response
    response = Response(content)
    response.headers['Cache-Control'] = 'public, max-age=3600'
    return response


@app.route('/getm3u8', methods=['GET'])
def getm3u8():
    source = decode_url(request.url.replace('https://lobster-app-bwfjt.ondigitalocean.app/getm3u8?source=', ''))
    
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
    
    response = session.get(source, headers=headers)
    content = response.text
    videoid = request.args.get("videoid")
    content = content.replace(videoid + '_', 'https://lobster-app-bwfjt.ondigitalocean.app/getstream?param=getts&source=https://edge10.xmediaget.com/hls-live/' + videoid + '/1/' + videoid + '_')

    # Add cache headers to the response
    response = Response(content)
    response.headers['Cache-Control'] = 'public, max-age=3600'
    return response


@app.route('/getstream', methods=['GET'])
def getstream():
    param = request.args.get("param")

    if param == "getts":
        source = decode_url(request.url.replace('https://lobster-app-bwfjt.ondigitalocean.app/getstream?param=getts&source=', ''))
        
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
        
        response = session.get(source, headers=headers)
        # Return with Content-Type set to image/jpg
        return Response(response.iter_content(chunk_size=128), content_type='image/jpg')
    
    if param == "getm3u8":
        videoid = request.args.get("videoid")
        veriler = {"AppId": "3", "AppVer": "1025", "VpcVer": "1.0.11", "Language": "tr", "Token": "", "VideoId": videoid}
        response = session.post("https://melbet-813981.top/cinema", json=veriler)

        if "FullscreenAllowed" in response.text:
            veri = re.findall('"URL":"(.*?)"', response.text)[0]
            veri = decode_url(veri.replace('edge3', 'edge10').replace('edge100', 'edge10').replace('edge4', 'edge10').replace('edge2', 'edge10').replace('edge5', 'edge10').replace('edge1', 'edge10').replace('edge6', 'edge10').replace('edge7', 'edge10').replace(':43434', '').replace('edge100', 'edge10'))

            if "m3u8" in veri:
                return "https://lobster-app-bwfjt.ondigitalocean.app/" + veri + '&videoid=' + videoid
        else:
            return "Veri yok"

    return "Parametre hatalı"


if __name__ == '__main__':
    app.run()
