#!/usr/bin/env bash

echo "Preparing the server..."
python -m venv venv
cd ./backend
source ./venv/bin/activate
pip install -r ./requirements.txt
python ./manage.py makemigrations
python ./manage.py migrate
echo "DONE Preparing"