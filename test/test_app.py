#指令 python -m pytest -vv

import pytest
import requests
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
                               "width": "100",
                               "height": "100"
                           })
    assert response.status_code == 200
    assert response.content_type == 'image/png'
    #要驗證png的的大小


def test_invalid_data(client):
    response = client.post('/generate_image',
                           json={
                               "width": "abc",
                               "height": "100"
                           })
    assert response.status_code == 400


def test_data_not_json(client):
    response = client.post('/generate_image', "test string")
    assert response.status_code == 400


def test_generate_image_not_json(client):
    response = client.post('/generate_image')
    assert response.status_code == 400


if __name__ == '__main__':
    pytest.main()
