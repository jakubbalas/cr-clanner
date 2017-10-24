from datetime import timedelta, datetime
from flask import render_template

from app import app
from app.models import Clan, WeekData, ClanPlayer


@app.route('/<clantag>')
def homepage(clantag):
    clan = Clan.query.filter_by(clantag=clantag).first()
    clan_players = ClanPlayer.query.filter_by(clan=clan, active=True)

    data = {}
    for player in clan_players:
        weeks = WeekData.query.filter_by(clan_player=player) \
            .order_by(WeekData.year, WeekData.week).limit(10).all()

        week_data = {}
        for week in weeks:
            weektag = "{}-{}".format(week.year, week.week)
            week_data[weektag] = week
        data[player.player.usertag] = week_data

    now = datetime.now()

    timetable = []
    for i in range(10):
        weekdiff = now - timedelta(weeks=i)
        timetable.append("{}-{}".format(
            weekdiff.isocalendar()[0],
            weekdiff.isocalendar()[1]))

    return render_template(
        "index.html",
        clan=clan,
        players = clan_players,
        timetable = timetable,
        data=data)
