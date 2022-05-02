#!/bin/bash

set -ex

python aggregator_project/manage.py get_token
python aggregator_project/manage.py runserver 0.0.0.0:8000
