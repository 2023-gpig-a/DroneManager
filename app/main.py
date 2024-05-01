import random
from enum import Enum
from typing import Tuple

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .area_resolution import TargetCircle
from .types import DroneId, LatLon

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # frontend dev
        "http://localhost:8080",  # frontend Docker
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DroneData(BaseModel):
    status: str
    battery: int
    lastUpdate: str
    lastSeen: LatLon


DRONE_STATUSES = ["idle", "flying", "unknown"]
DRONES: dict[DroneId, DroneData] = dict()
DRONE_VISION = 1.0

ROUTES_QUEUE: list[list[LatLon]] = []


@app.get("/")
async def hello_world():
    return {"response": "Hello World"}


# get the status (position) of all the drones
# called by the frontend
@app.get("/drone_status")
async def get_drone_status() -> dict[DroneId, DroneData]:
    return DRONES


@app.get("/drone_status/{id}")
async def get_individual_drone(id: DroneId) -> DroneData:
    # TODO: handle KeyErrors better
    return DRONES[id]


ROUTING_METHOD = TargetCircle.path_method1


# send the drone fleet to search a particular area
# currently only supports a circle
# called by the frontend
@app.post("/drone_dispatch/circle")
async def drone_dispatch_circle(target: TargetCircle) -> None:
    ROUTES_QUEUE.append(ROUTING_METHOD(target, DRONE_VISION))
    return


# update the stored status of a drone
# called by the drone simulation
@app.post("/drone_status/{id}")
async def update_drone_status(id: DroneId, drone: DroneData) -> None:
    DRONES[id] = drone
    return


# retrieve the next sequence of points that a drone needs to go and "scan"
# called by the drone simulation
@app.get("/next_area")
async def get_next_drone_area() -> list[LatLon]:
    return ROUTES_QUEUE.pop()
