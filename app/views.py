from flask import render_template

from app import app


@app.route('/')
def homepage():
    data = []
    return render_template("index.html", data=data)
