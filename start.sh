#!/bin/bash

# this is the docker entrypoint file

echo "start.sh..."

# go to the directory where the files are mounted:
cd /root/app

# create python virtual environment:
python -m venv ./venv

# activate python virtual environment:
source ./venv/bin/activate

# install the app + dependencies:
python -m pip install -e .

# run the app:
python ./main.py
