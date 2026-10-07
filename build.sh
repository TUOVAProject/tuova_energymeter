#!/bin/bash

# this script gathers all the stuff needed for deployment to ./build

rm -rf ./build
mkdir -p ./build

cp -r ./config.json ./main.py ./pyproject.toml ./README.md ./src ./docker-compose.yml ./.python-version ./uv.lock ./start.sh ./build
rm -rf ./build/src/tuova_energymeter/__pycache__
rm -rf ./build/src/__pycache__
rm -rf ./build/__pycache__
