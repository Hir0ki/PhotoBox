#!/usr/bin/env bash

# unmount auto mounted camera
gio mount -s gphoto2

# start app
source ./venv/bin/activate
python3 ./main.py