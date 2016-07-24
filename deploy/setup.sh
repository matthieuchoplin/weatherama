#!/usr/bin/env bash
pip install -r ././../requirements.txt
npm install -g bower
python ././../manage.py bower_install
python ././../manage.py collectstatic --no-input
