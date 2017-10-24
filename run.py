#!bin/python
from app import app
from app.db import db
import os

debug = os.environ['APP_ENV'] not in ['production', 'integration']
db.init_app(app)
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=debug)
