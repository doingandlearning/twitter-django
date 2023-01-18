#!/usr/bin/env bash 
set -o errexit

poetry install
poetry shell
python manage.py migrate