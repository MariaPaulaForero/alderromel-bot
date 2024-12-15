from typing import Union
import asyncio


from fastapi import FastAPI, WebSocket
from fastapi.testclient import TestClient
from geojson import Point
from pydantic import BaseModel
from gps.main import get_gps_location
from camera.main import get_image
from constants import is_simulation_mode, simulated_base64_image

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
    print("control_robot")
    print(command)

    global motor_thread
    action = command.action.lower()

    if (is_simulation_mode):
        return {"status": "success", "action": action}

    # Stop any ongoing motor control before starting a new one
    if motor_thread is not None and motor_thread.is_alive():
        stop_motors()
        motor_thread.join()  # Wait for the thread to finish

    # Start a new thread to control the motors
    motor_thread = threading.Thread(target=control_motors, args=(action,))
    motor_thread.start()

    return {"status": "success", "action": action}


@app.websocket('/current-location')
async def current_location(websocket: WebSocket):
    await websocket.accept()
    # Raspberry gps

    while True:
        gps_location = get_gps_location()

        gps_point = Point((gps_location['lng'], gps_location['lat']))
            
        await asyncio.sleep(1)
        await websocket.send_json(gps_point)

@app.websocket("/camera")
async def websocket_kamavinga(websocket: WebSocket):
    await websocket.accept()
    
    width, height = 640, 500

    try:
        while True:
            image = get_image()
            await websocket.send_text(image)
            await asyncio.sleep(0.05)  # Controla la tasa de envío
    except Exception as e:
        print(f"Error: {e}")                
