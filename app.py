import requests
from flask import Flask, request
from flask_cors import CORS
import re
 
app = Flask(__name__)
CORS(app)
 
@app.route('/<m3u8>')
def index(m3u8):
    return "Gerekli işlemleri yapmak için bu URL'i kullanabilirsiniz: /getts?m3u8=" + m3u8
 
@app.route('/getts', methods=['GET'])
def get_ts():
    m3u8 = request.args.get('m3u8')
    m3u8 = m3u8.replace('__', '/')
    source = m3u8.replace('https://erdoganladevam.herokuapp.com/', '')
    source = source.replace('%2F', '/')
    source = source.replace('%3F', '?')
    videoid = request.args.get('videoid')
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'tr-TR, tr;q=0.9',
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
    ts = requests.get(source, headers=headers)
    tsal = ts.text.replace(videoid+'_', f'https://cors-proxy.fringe.zone/https://erdoganladevam.herokuapp.com/getstream?param=getts&source=https://edge10.xmediaget.com/hls-live/{videoid}/1/{videoid}_')
    if 'internal' in tsal:
        tsal = tsal.replace('internal', f'https://cors-proxy.fringe.zone/https://erdoganladevam.herokuapp.com/getstream?param=getts&source=https://edge10.xmediaget.com/hls-live/{videoid}/1/internal')
    if 'segment' in tsal:
        tsal = tsal.replace('\nmedia', f'\nhttps://cors-proxy.fringe.zone/https://erdoganladevam.herokuapp.com/getstream?param=getts&source=https://edge10.xmediaget.com/hls-live/{videoid}/1/media')
    return tsal
 
@app.route('/getm3u8', methods=['GET'])
def get_m3u8():
    source = request.args.get('source')
    source = source.replace('%2F', '/')
    source = source.replace('%3F', '?')
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'tr-TR, tr;q=0.9',
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
    ts = requests.get(source, headers=headers)
    tsal = ts.text
    tsal = tsal.replace(videoid+'_','https://erdoganladevam.herokuapp.com/getstream?param=getts&source=https://edge10.xmediaget.com/hls-live/'+videoid+'/1/'+videoid+'_')
    return tsal
 
@app.route('/getstream', methods=['GET'])
def get_stream():
    param = request.args.get("param")
    if param == "getts":
        source = request.args.get("source")
        source = source.replace('https://erdoganladevam.herokuapp.com/getstream?param=getts&source=','')
        source = source.replace('%2F','/')
        source = source.replace('%3F','?')
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
        ts = requests.get(source, headers=headers)
        return ts.content
    return "Geçersiz parametre"
 
if __name__ == '__main__':
    app.run()
