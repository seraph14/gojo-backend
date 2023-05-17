#!/usr/bin/env bash

echo "Running the server..."
cd ./backend
source ./venv/bin/activate
python ./manage.py runserver