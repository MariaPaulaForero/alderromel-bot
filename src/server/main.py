from typing import Union
import asyncio


from fastapi import FastAPI, WebSocket
from fastapi.testclient import TestClient
from geojson import Point
from pydantic import BaseModel
from gps.main import get_gps_location
from camera.main import get_image
from constants import is_simulation_mode, simulated_base64_image
from motor.engine_test import backward, forward, turn_left, turn_right, stop
from motor.ball_follower import dogStep
import cv2

app = FastAPI()
camera = cv2.VideoCapture(0)

class Command(BaseModel):
    action: str

class CommandSpeed(BaseModel):
    movement_speed: int

class CommandMode(BaseModel):
    movement_mode: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

import threading
import time

# Global variable to control the motor state
running = False
motor_thread = None
movement_mode = "control" # control, dog, map, path
movement_speed = 100 # esta es la velocidad teorica a la que podemos ajustar el robot desde el frontend

def control_motors(action):
    global running
    running = True

    while running:
        '''
        if (movement_mode == "dog"):
            print("antes del dog step")
            dogStep()
            print("despues del dog step")
    
        else:
        '''          
        if action == "forward":
            forward(movement_speed, movement_speed)
        elif action == "backward":
            backward(movement_speed, movement_speed)
        elif action == "turn_left":
            turn_left(movement_speed, 0)
        elif action == "turn_right":
            turn_right(0, movement_speed)
        elif action == "stop":
            #stop()
            stop_motors()
        else:
            stop_motors()
        time.sleep(0.1)  # Adjust the sleep time as needed

def dog_control(camera):
    global running
    running = True

    print("running dog_control")
  
    while running:
      print("runnign dog_control")  
      aux = dogStep(camera)
      if (aux == False):
        stop_motors()
        break

def stop_motors():
    global running
    running = False
    stop()  # Ensure motors are stopped when exiting

def get_current_status():
    return {
        "movement_mode": movement_mode,
        "running": running,
        "movement_speed": movement_speed
    }

# Example usage in your FastAPI endpoint
@app.get("/current-status")
async def current_status():
    return {
        "status": "success",
        "current_status": get_current_status()
    }

# Change speed endpoint
@app.put("/change-speed")
async def change_speed(command: CommandSpeed):
    print("movement_speed")
    print(command)

    global movement_speed
    movement_speed = command.movement_speed

    return {
            "status": "success",
            "speed": movement_speed,
            "current_status": get_current_status()
        }

# Change movementMode endpoint
@app.put("/change-mode")
async def change_movement_mode(command: CommandMode):
    global camera
    print("movement_mode")
    print(command)
    global motor_thread
    
    # validate its control, dog or map
    if command.movement_mode not in ["control", "dog", "map", "path"]:
        return {
            "status": "error",
            "message": "Invalid movement mode"
        }

    global movement_mode
    movement_mode = command.movement_mode

    # Stop any ongoing motor control before starting a new one
    if motor_thread is not None and motor_thread.is_alive():
        stop_motors()
        motor_thread.join()  # Wait for the thread to finish

    if (movement_mode == "dog"):
        # Start a new thread to control the motors
        motor_thread = threading.Thread(target=dog_control, args=(camera,))
        motor_thread.start()

    return {
            "status": "success",
            "mode": movement_mode,
            "current_status": get_current_status()
        }

# Control bot endpoint
@app.post("/control-robot")
async def control_robot(command: Command):
    print("control_robot")
    print(command)

    global motor_thread
    action = command.action.lower()

    if (is_simulation_mode):
        return {
            "status": "success",
            "action": action,
            "current_status": get_current_status()
        }

    # Stop any ongoing motor control before starting a new one
    if motor_thread is not None and motor_thread.is_alive():
        stop_motors()
        motor_thread.join()  # Wait for the thread to finish

    if (movement_mode == "control"):
        # Start a new thread to control the motors
        motor_thread = threading.Thread(target=control_motors, args=(action,))
        motor_thread.start()

    return {
            "status": "success",
            "action": action,
            "current_status": get_current_status()
        }

@app.websocket('/current-location')
async def current_location(websocket: WebSocket):
    await websocket.accept()
    # Raspberry gps

    while True:
        gps_location = get_gps_location()

        gps_point = Point((gps_location['lng'], gps_location['lat']))
            
        await asyncio.sleep(1)
        await websocket.send_json({
            "coordinates": gps_point,
            "orientation": gps_location['orientation'],
            "speed": gps_location['speed'], # a diferencia de la velocidad teorica, esta es la velocidad del GPS, no se ajusta, se mide
        })

@app.websocket("/socket-camera")
async def websocket_kamavinga(websocket: WebSocket):
    global camera
    await websocket.accept()
    
    width, height = 640, 500

    try:
        while True:
            image = get_image(camera)
            await websocket.send_text(image)
            await asyncio.sleep(0.05)  # Controla la tasa de envío
    except Exception as e:
        print(f"Error: {e}")                
