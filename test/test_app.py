import pytest
import json
from PIL import Image
from io import BytesIO

from app.main import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_generate_image(client):
    response = client.post('/generate_image',
                           json={
                               "width": "1920",
                               "height": "1080"
                           })
    assert response.status_code == 200
    assert response.content_type == 'image/png'
    # Check the image size
    image_data = BytesIO(response.data)
    image = Image.open(image_data)
    assert image.width == 1920
    assert image.height == 1080


def test_invalid_data(client):
    response = client.post('/generate_image',
                           json={
                               "width": "abc",
                               "height": "100"
                           })
    jsonResponse = json.loads(response.text)
    assert response.status_code == 400
    assert jsonResponse['data-error'] == 'request data contains non-number elements'

def test_data_not_json(client):
    response = client.post('/generate_image', "test string")

    jsonResponse = json.loads(response.text)
    assert response.status_code == 400
    assert jsonResponse['data-error'] == 'request data not JSON format'


def test_generate_image_not_json(client):
    response = client.post('/generate_image')

    jsonResponse = json.loads(response.text)
    assert response.status_code == 400
    assert jsonResponse['data-error'] == 'request data not JSON format'


if __name__ == '__main__':
    pytest.main()
