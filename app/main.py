import random
from enum import Enum
from typing import Dict, List, Tuple

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

DroneId = str
LatLon = Tuple[float, float]


class DroneData(BaseModel):
    status: str
    battery: int
    lastUpdate: str
    lastSeen: LatLon


DRONE_STATUSES = ["idle", "flying", "unknown"]
DRONES: Dict[DroneId, DroneData] = dict()


@app.get("/")
async def hello_world():
    return {"response": "Hello World"}


# get the status (position) of all the drones
# called by the frontend
@app.get("/drone_status")
async def get_drone_status() -> List[Tuple[DroneId, DroneData]]:
    DRONE_QUANTITY = 5
    DRONE_CENTER = [54.39, -0.937]

    # TODO: send from internal storage
    def create_random_drone(id: DroneId) -> Tuple[DroneId, DroneData]:
        return (
            id,
            DroneData(
                status=str(random.choice(DRONE_STATUSES)),
                battery=random.randint(0, 100),
                lastUpdate="",
                lastSeen=(
                    DRONE_CENTER[0] + random.random() * 0.05,
                    DRONE_CENTER[1] + random.random() * 0.05,
                ),
            ),
        )

    return [create_random_drone(str(i + 1)) for i in range(DRONE_QUANTITY)]


class TargetCircle(BaseModel):
    lat: float
    lon: float
    radius: float


# send the drone fleet to search a particular area
# currently only supports a circle
# called by the frontend
@app.post("/drone_dispatch/circle")
async def drone_dispatch_circle(target: TargetCircle) -> None:
    pass


# update the stored status of a drone
# called by the drone simulation
@app.post("/drone_status/{id}")
async def update_drone_status(id: DroneId, drone: DroneData) -> None:
    pass


# retrieve the next sequence of points that a drone needs to go and "scan"
# called by the drone simulation
@app.get("/next_area")
async def get_next_drone_area() -> List[LatLon]:
    pass
