from typing import Union

from fastapi import FastAPI, WebSocket
from fastapi.testclient import TestClient
from geojson import Point
from motor.engine_test import backward, forward, turn_left, turn_right, stop
from pydantic import BaseModel
from gps.main import get_gps_location

app = FastAPI()


class Command(BaseModel):
    action: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

import threading
import time

# Global variable to control the motor state
running = False
motor_thread = None

def control_motors(action):
    global running
    running = True

    while running:
        if action == "forward":
            forward()
        elif action == "backward":
            backward()
        elif action == "turn_left":
            turn_left()
        elif action == "turn_right":
            turn_right()
        elif action == "stop":
            stop()
        else:
            stop_motors()

        time.sleep(0.1)  # Adjust the sleep time as needed

def stop_motors():
    global running
    running = False
    stop()  # Ensure motors are stopped when exiting

# Example usage in your FastAPI endpoint
@app.post("/control-robot")
async def control_robot(command: Command):
    global motor_thread
    action = command.action.lower()

    # Stop any ongoing motor control before starting a new one
    if motor_thread is not None and motor_thread.is_alive():
        stop_motors()
        motor_thread.join()  # Wait for the thread to finish

    # Start a new thread to control the motors
    motor_thread = threading.Thread(target=control_motors, args=(action,))
    motor_thread.start()

    return {"status": "success", "action": action}


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
