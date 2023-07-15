import random
import logging
import google.cloud.logging
from flask import Flask, request, send_file, jsonify, abort
from PIL import Image

app = Flask(__name__)

#log config
client = google.cloud.logging.Client()
client.setup_logging()
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s %(levelname)-8s] %(message)s',
    datefmt='%Y%m%d %H:%M:%S',
)


@app.route('/generate_image', methods=['POST'])
def generate_image():
    if request.is_json:
        data = request.get_json()
        width = data.get('width')
        height = data.get('height')
        if not height.isnumeric() or not width.isnumeric():
            logging.DEBUG("request data contain not number element")
            content = {
                'data-error': "please use number with width and height "
            }
            return jsonify(content), 400
    else:
        logging.DEBUG("request data not json")
        content = {'data-error': "request data should be json"}
        return jsonify(content), 400

    try:
        image = Image.new('RGB', (int(width), int(height)), (random.randint(
            0, 255), random.randint(0, 255), random.randint(0, 255)))
        temp_filename = 'temp.png'
        image.save(temp_filename, 'PNG')
        return send_file(temp_filename, mimetype='image/png'), 200
    except:
        logging.ERROR("server error")
        content = {'error': "server error"}
        return jsonify(content), 500


if __name__ == '__main__':
    app.run()
