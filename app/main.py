import random
import logging
import google.cloud.logging
from flask import Flask, request, send_file, jsonify, abort
import uuid
import requests
import json
from PIL import Image

app = Flask(__name__)
GA_url = f'https://www.google-analytics.com/mp/collect?measurement_id=G-46978BE92P&api_secret=BcsrljfJTnqTGXndMPVgyA'

#log config 放上GCP拿掉
"""
client = google.cloud.logging.Client()
client.setup_logging()
"""

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s %(levelname)-8s] %(message)s',
    datefmt='%Y%m%d %H:%M:%S',
)


def send_log＿to_GA(err):
    try:
        payload = {
            'client_id': '111.111',
            'events': [{
                'name': 'yoooooo',
                'params': {
                    'ok':'true'
                },
            }]
        }
        headers = {'Content-type': 'application/json'}
        r=requests.post(GA_url,
                      headers=headers,
                      data=json.dumps(payload),
                      verify=True)
        logging.warning(r)
    except requests.exceptions.RequestException as e:
        logging.warning(e)


def generate_image(width, height):
    try:
        image = Image.new('RGB', (int(width), int(height)), (random.randint(
            0, 255), random.randint(0, 255), random.randint(0, 255)))
        temp_filename = 'temp.png'
        image.save(temp_filename, 'PNG')
        return send_file(temp_filename, mimetype='image/png')
    except:
        logging.ERROR("server error")
        content = {'error': "server error"}
        return jsonify(content), 500


@app.route('/generate_image', methods=['POST'])
def generate_image_route():
    if request.is_json:
        data = request.get_json()
        width = data.get('width')
        height = data.get('height')
        if not height.isnumeric() or not width.isnumeric():
            err = "request data contains non-number elements"
            logging.warning(err)
            send_log_to_GA(err)
            content = {'data-error': err}
            return jsonify(content), 400
    else:
        logging.warning("request data not in JSON format")
        content = {'data-error': "request data should be JSON"}
        return jsonify(content), 400

    return generate_image(width, height)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
