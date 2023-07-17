#-*-coding:UTF-8-*-
import random
import logging
import requests
import json
import google.cloud.logging
from datetime import datetime
from flask import Flask, request, send_file, jsonify, abort
from PIL import Image

app = Flask(__name__)
GA_url = 'https://www.google-analytics.com/mp/collect?measurement_id=G-46978BE92P&api_secret=BcsrljfJTnqTGXndMPVgyA'

#google cloud log config - local test don't need
"""
client = google.cloud.logging.Client()
client.setup_logging()
"""

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s %(levelname)-8s] %(message)s',
    datefmt='%Y%m%d %H:%M:%S',
)


def send_log_to_GA(err):
    try:
        now = datetime.now()
        time = datetime.strftime(now, "%Y-%m-%d %H:%M:%S")
        mes = time + ": " + err
        payload = {
            'client_id': 'junis',
            'events': [{
                'name': 'log',
                'params': {
                    'log': mes
                },
            }]
        }
        headers = {'Content-type': 'application/json'}
        r = requests.post(GA_url,
                          headers=headers,
                          data=json.dumps(payload),
                          verify=True)
    except requests.exceptions.RequestException as e:
        logging.warning("Send data to GA event fail")


def generate_image(width, height):
    try:
        image = Image.new('RGB', (int(width), int(height)), (random.randint(
            0, 255), random.randint(0, 255), random.randint(0, 255)))
        temp_filename = 'temp.png'
        image.save(temp_filename, 'PNG')
        return send_file(temp_filename, mimetype='image/png')
    except:
        err = "server generate image fail"
        logging.ERROR(err)
        send_log_to_GA(err)
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
        err = "request data not JSON format"
        logging.warning(err)
        send_log_to_GA(err)
        content = {'data-error': err}
        return jsonify(content), 400

    return generate_image(width, height)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
