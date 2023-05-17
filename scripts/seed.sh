#!/usr/bin/env bash

echo "seed db"
cd ./backend
source venv/bin/activate
python manage.py flush
echo "Generating Fake Data"
python manage.py fake_data
echo "Data Generated! 🐒"