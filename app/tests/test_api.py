from fastapi.testclient import TestClient
from main import app
from app.api.models import Meme

client = TestClient(app)


def test_get_memes():
    response = client.get('/memes')
    assert response.status_code == 200
    assert response.json() != []


def test_get_meme():
    response = client.get('/memes/1')
    assert response.status_code == 200
    assert response.json() != {}


def test_create_meme():
    image_file = (b'fake_image', 'image.jpg')
    text = 'This is a test meme'
    response = client.post('/memes', json={'text': text}, files={'image': image_file})
    assert response.status_code == 201
    assert response.json() != {}


def test_update_meme():
    meme = Meme(id=1, image_url='http://example.com/image.jpg', text='This is a test meme')
    response = client.put('/memes/1', json=meme.dict())
    assert response.status_code == 200
    assert response.json()['text'] == 'This is a test meme'


def test_delete_meme():
    response = client.delete('/memes/1')
    assert response.status_code == 200
