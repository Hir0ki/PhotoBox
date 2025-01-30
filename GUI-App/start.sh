#!/usr/bin/env bash

# unmount auto mounted camera
#gio mount -s gphoto2

# 
export DISPLAY=:0.0

# start app
source ./venv/bin/activate
python3 ./main.py
#gdb --args python3 ./main.py
