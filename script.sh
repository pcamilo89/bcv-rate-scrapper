#!/bin/bash

# Optional for desktop notifications
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus
export DISPLAY=:0

fullpath="/absolute/path/to/project"

cd $fullpath

source "./venv/bin/activate"

python "./src/web_scrap.py" auto

deactivate
