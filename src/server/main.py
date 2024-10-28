from typing import Union

from fastapi import FastAPI, WebSocket
from fastapi.testclient import TestClient
from geojson import Point

from gps.main import get_gps_location

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.websocket('/ws')
async def websocket(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({ "msg": "Hello WebSocket" })
    await websocket.close()

@app.get('/test-ws')
def test_websocket():
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        data = websocket.receive_json()
        return data

@app.websocket('/current-location')
async def current_location(websocket: WebSocket):
    await websocket.accept()
    # Raspberry gps
    gps_location = get_gps_location()

    gps_point = Point((gps_location['lng'], gps_location['lat']))

    await websocket.send_json(gps_point)

    await websocket.close()

@app.get('/test-current-location')
def test_current_location():
    client = TestClient(app)
    with client.websocket_connect("/current-location") as websocket:
        data = websocket.receive_json()
        return data
