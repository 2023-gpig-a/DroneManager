# Drone Manager

This system is responsible for the following:

## Running without docker
```
python3 -m venv venv
. venv/bin/activate (linux) or ./venv/Scripts/activate (win)
python3 -m pip install -e
pip install -r requirements.txt
uvicorn dronemanager.app.main:app --reload
```

## Running with docker
```
docker build -t drone_manager_image .
docker run -d --name dronemanager -p 8080:8080 drone_manager_image
```

## Endpoints:

`/get_drone_status`