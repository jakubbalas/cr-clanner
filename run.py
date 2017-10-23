#!bin/python
from app import app
from app.db import db
import os

debug = os.environ['APP_ENV'] not in ['production', 'integration']

if __name__ == '__main__':
    db.init_app(app)
    app.run(host='0.0.0.0', debug=debug)
