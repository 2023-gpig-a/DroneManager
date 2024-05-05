# Drone Manager

This system is responsible for interfacing between the frontend systems and the drone management software provided by manufacturers.

It takes areas of interest and resolves them into search patterns to photograph for the backend drone software.
It also allows the frontend to get information about the drones' statuses.

## Running without docker

```bash
python3 -m venv venv
. venv/bin/activate # linux
./venv/Scripts/activate # windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Running with docker

```bash
docker build -t drone_manager_image .
docker run -d --name dronemanager -p 8080:8080 drone_manager_image
```

## Endpoints

You can view the endpoints and accompanying API doc by running the service, then going to `http://hostname:port/docs`.

## Test Suite

You can run the tests with:

```bash
. venv/bin/activate && python3 -m unittest discover -s tests # linux
./venv/Scripts/activate && python3 -m unittest discover -s tests # windows
```
