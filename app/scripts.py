import click
from datetime import datetime

from app import app
from app.db import db


@app.cli.command()
def load_weeks_data():
    """Run this the first time you deploy"""
    command = InitCommand()
    command.init_app()


@app.cli.command()
def dev_insert_fixtures():
    """Initialize the database."""
    command = DevCommands()
    command.dev_insert_fixturess()

