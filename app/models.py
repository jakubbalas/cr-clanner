import bcrypt

from app.db import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'clanner_user'  # User is often a keyword in SQL

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String, nullable=True)

    name = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)

    def set_password(self, password):
        password = bcrypt.hashpw(password.encode("utf"), bcrypt.gensalt())
        self.password = password.decode("utf")
        return self.password

    def check_password(self, password):
        return bcrypt.checkpw(
            password.encode("utf"),
            self.password.encode("utf")
        )

    def __repr__(self):
        return '<User %r>' % self.username


class Clan(db.Model):
    __tablename__ = 'clan'

    id = db.Column(db.Integer, primary_key=True)
    clantag = db.Column(db.String(20), index=True, unique=True)
    name = db.Column(db.String(64), unique=False)


class Player(db.Model):
    __tablename__ = 'player'

    id = db.Column(db.Integer, primary_key=True)
    usertag = db.Column(db.String(20), index=True, unique=True)
    name = db.Column(db.String(64), unique=False)
    trophies = db.Column(db.Integer)
    level = db.Column(db.Integer)


class ClanPlayer(db.Model):
    __tablename__ = 'clan_player'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20))
    active = db.Column(db.Boolean, default=False)

    player = db.relationship('Player', backref='clan', uselist=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))

    clan = db.relationship('Clan', backref='players')
    clan_id = db.Column(db.Integer, db.ForeignKey('clan.id'))


class WeekData(db.Model):
    __tablename__ = 'week_data'

    id = db.Column(db.Integer, primary_key=True)
    donations = db.Column(db.Integer)
    crowns = db.Column(db.Integer)
    year = db.Column(db.Integer)
    week = db.Column(db.Integer)

    clan_player = db.relationship('ClanPlayer', backref='data')
    clan_player_id = db.Column(db.Integer, db.ForeignKey('clan_player.id'))
