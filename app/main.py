import random
from enum import Enum
from typing import Tuple

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

DRONE_QUANTITY = 5
DRONE_CENTER = [54.39, -0.937]
DRONE_STATUSES = ["idle", "flying", "unknown"]

LatLon = Tuple[float, float]


@app.get("/")
async def hello_world():
    return {"response": "Hello World"}


class DroneData(BaseModel):
    id: str
    status: str
    battery: int
    lastUpdate: str
    lastSeen: Tuple[float, float]


# get the status (position) of all the drones
# called by the frontend
@app.get("/drone_status")
async def get_drone_status():
    # TODO: send from internal storage
    def create_random_drone(id: str):
        data = DroneData(
            id=id,
            status=str(random.choice(DRONE_STATUSES)),
            battery=random.randint(0, 100),
            lastUpdate="",
            lastSeen=(
                DRONE_CENTER[0] + random.random() * 0.05,
                DRONE_CENTER[1] + random.random() * 0.05,
            ),
        )
        return data

    drones = [create_random_drone(str(i + 1)) for i in range(DRONE_QUANTITY)]

    return drones


# send the drone fleet to search a particular area
# currently only supports a circle
# called by the frontend
@app.post("/drone_dispatch")
async def drone_dispatch(target: LatLon, radius: float):
    pass


# notify that a drone has moved
# called by the drone simulation
@app.post("/drone_status")
async def update_drone_status(position: LatLon):
    pass
