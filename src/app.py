from flask import Flask, abort, request
import logging
from urllib.parse import urljoin
import io
import requests
from models.plate_reader import PlateReader

app = Flask(__name__)
plate_reader_model = PlateReader.load_from_file('model_weights/plate_reader_model.pth')
AVAILABLE_IDS = ['10022', '9965']


class DownloadImageException(Exception):
    pass

def check_is_available(id):
    if id not in AVAILABLE_IDS:
        abort(404, description=f'image {id} is not available')
    return True

def download_image(id):
    SERVICE_URL = 'http://51.250.83.169:7878/images/'
    download_url = urljoin(SERVICE_URL, id)
    
    with requests.get(download_url, stream=True) as r:
        if r.status_code == 200:
            return io.BytesIO(r.raw.read())
        else:
            raise DownloadImageException

def get_image(id):
    try:
        im = download_image(id)
    except DownloadImageException:
        abort(503, description=f'failed to download image {id}')
    except:
        abort(500, description=f'unknown server error')

    return im

@app.route('/readPlateImage/<id>')
def read_plate_image(id : str):
    check_is_available(id)
    im = get_image(id)
    res = plate_reader_model.read_text(im)
    return {'result' : res}

@app.route('/readPlateImages', methods=['POST', 'GET'])
def read_plate_images():
    if 'ids' not in request.json:
        abort(400, description=f'invalid args: ids not in args')
    
    ids = request.json['ids']
    results = {}
    for id in ids:
        check_is_available(id)
        im = get_image(id)
        res = plate_reader_model.read_text(im)
        results[id] = res

    return {'result': results}


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s] %(message)s',
        level=logging.INFO,
    )

    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=8080, debug=True)
