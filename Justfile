#!/bin/env -S just --justfile

set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

DIMAGE := "gpig/dmas"
# prefer podman over docker
DOCKER := if `podman --version || echo nope` == "nope" {
    "docker"
} else {
    "podman"
}

VENV_LOC := "venv"
VENV_ACT := if os() == "windows" {
    VENV_LOC + "/Scripts/activate && "
} else {
    "source " + VENV_LOC + "/bin/activate && "
}

# prefer uv over default pip and venv
VENV_TOOL := if `uv --version || echo nope` == "nope" {
    "python3 -m venv"
} else {
    "uv venv"
}
PIP := VENV_ACT + if `uv --version || echo nope` == "nope" {
    "pip"
} else {
    "uv pip"
}

# run the service
run port="8080" host="127.0.0.1" *args="--reload": venv test
    {{ VENV_ACT }} uvicorn \
        --host "{{ host }}" \
        --port "{{ port }}" \
        {{ args }} \
        app.main:app
alias r := run

# get a python shell, dependencies and project loaded
shell: venv
    {{ VENV_ACT }} python -ic 'import app'

# run the service in a container
drun port="8080" *dargs="": dbuild
    {{ DOCKER }} run \
        --rm \
        -p "{{ port }}:8080" \
        {{ dargs }} \
        "{{ DIMAGE }}"
alias dr := drun

# get an interactive shell in the docker container
ddebug port="8080": (drun port "--entrypoint" "/bin/bash" "-it")

# build the docker container
dbuild: test
    {{ DOCKER }} build -t "{{ DIMAGE }}" .

# create the venv and install dependencies
venv:
    {{ VENV_TOOL }} "{{ VENV_LOC }}"
    {{ PIP }} install -r requirements.txt

# run the formatter over the working directory
format:
    black .

# run linter(s)
lint:
    @# we don't have an exclude for black because it respects gitignore
    black --check .
    mypy --exclude "{{ VENV_LOC }}" . || exit 0
    rg -g '!Justfile' TODO
alias l := lint

# run the test suite
test:
    {{ VENV_ACT }} python3 -m unittest discover ./tests
alias t := test
