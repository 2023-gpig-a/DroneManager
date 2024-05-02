import random
from enum import Enum
from typing import Tuple

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .area_resolution import TargetCircle
from .types import DroneId, LatLon

app = FastAPI(
    title="Drone Manager",
    summary="Middle layer between frontend systems and manufacturer drone interfaces.",
    description="""Drone Manager is a service which interfaces between abstracted frontend systems which wish to instruct drones to photograph particular areas (and get regular updates), and the systems provided by drone manufacturers to allow remote instruction of drone flight controllers.
It is intended to provide an abstraction layer over different drone models.

Endpoints are provided for the frontend systems to call to instruct the fleet and get updates on their positions and progress; these are:

- `GET /drone_status*`
- `POST /drone_dispatch*`

Endpoints for drone controllers are:

- `POST /drone_status*`
- `GET /next_area`

See respective endpoints for full documentation.
    """,
)

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


@app.get("/", summary="Hello world sanity check.")
async def hello_world():
    return {"response": "Hello World"}


@app.get(
    "/drone_status",
    summary="Get all known information about all drones in the field.",
    description="Intended for frontend usage.",
)
async def get_drone_status() -> dict[DroneId, DroneData]:
    return DRONES


@app.get(
    "/drone_status/{id}",
    summary="Get all known information about a particular drone, given it's id.",
    description="Intended for frontend usage.",
)
async def get_individual_drone(id: DroneId) -> DroneData:
    # TODO: handle KeyErrors better
    return DRONES[id]


ROUTING_METHOD = TargetCircle.path_method1


@app.post(
    "/drone_dispatch/circle",
    summary="Add a circular area to the queue for drones to search.",
    description="Intended for frontend usage.",
)
async def drone_dispatch_circle(target: TargetCircle) -> None:
    ROUTES_QUEUE.append(ROUTING_METHOD(target, DRONE_VISION))
    return


@app.post(
    "/drone_status/{id}",
    summary="Update the known status of a drone.",
    description="""This updates the internal cache of this service, and will be served with the `GET /drone_status` endpoints.
Intended for backend usage.""",
)
async def update_drone_status(id: DroneId, drone: DroneData) -> None:
    DRONES[id] = drone
    return


# retrieve the next sequence of points that a drone needs to go and "scan"
# called by the drone simulation
@app.get(
    "/next_area",
    summary="Retrieve the next sequence of points in the queue for a drone to photograph.",
    description="""**NOTE**: this sequence of points is the *minimal* routing path.
The drone **must** self-instruct on when photographs are taken, eg. whenever it's out of range of the last photo taken, instead of just taking one at each node.""",
)
async def get_next_drone_area() -> list[LatLon]:
    return ROUTES_QUEUE.pop()
