#!/usr/bin/env bash 
set -o errexit

poetry install

python manage.py migrate