#!/bin/bash
export FLASK_APP="/app/run.py"
export LC_ALL="C.UTF-8"
export LANG="C.UTF-8"

/etc/init.d/cron start
flask run --host=0.0.0.0 --port=5000
