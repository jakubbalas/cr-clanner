from datetime import datetime, timedelta
import re
import json
import click
import requests
from bs4 import BeautifulSoup
from pytz import timezone


from app import app
from app.db import db
from .models import Clan, Player, ClanPlayer, WeekData


@app.cli.command()
def load_data():
    """Load data from the source"""

    # Define which div holds the data
    row_map = {
        "usertag": 1,
        "name": 1,
        "role": 12,
        "crowns": 9,
        "donations": 11,
        "trophies": 7,
        "level": 2
    }

    cutoff_minute = 8 * 60
    db.init_app(app)
    clans = Clan.query.all()
    source = "https://statsroyale.com/clan/{tag}"
    refresh_source = "{source}/refresh"


    for clan in clans:
        clanstats = source.format(tag=clan.clantag)

        req = requests.get(clanstats)

        a = json.loads(re.search(r'{"csrfToken":"\w+"}', req.text).group(0))
        cookie = {'XSRF-TOKEN': a["csrfToken"]}
        clan_refresh_source = refresh_source.format(source=clanstats)
        requests.get(clan_refresh_source, cookies=cookie)

        req = requests.get(clanstats)
        data = req.text
        soup = BeautifulSoup(data, 'html.parser')

        rows = soup.find_all("div", "clan__rowContainer")

        active_players = []
        now = datetime.now(tz=timezone("Europe/London"))
        last_week = now - timedelta(weeks=1)
        for row in rows:
            rowdata = row.find_all("div")

            # Create or update Player
            usertag = rowdata[row_map["usertag"]].a['href'][9:]
            player = Player.query.filter_by(usertag=usertag).first()
            if player is None:
                player = Player(usertag=usertag)
            active_players.append(player)
            player.name = rowdata[row_map["name"]].a.text.strip()
            player.trophies = int(rowdata[row_map["trophies"]].text)
            player.level = int(rowdata[row_map["level"]].span.text)

            db.session.add(player)
            db.session.commit()

            # Get Clan Player
            clan_player = None
            # Make sure that it is only in this clan now.
            for cp in ClanPlayer.query.filter_by(player=player).all():
                if cp.active is True and cp.clan.id != clan.id:
                    cp.active = False
                    db.session.add(cp)
                    db.seesion.commit()
                elif cp.clan.id == clan.id:
                    clan_player = cp

            if clan_player is None:
                clan_player = ClanPlayer(player=player, clan=clan)

            clan_player.role = rowdata[row_map["role"]].text.strip()
            clan_player.active = True

            db.session.add(clan_player)
            db.session.commit()

            this_data = WeekData.query.filter_by(
                clan_player=clan_player,
                year=now.isocalendar()[0],
                week=now.isocalendar()[1]
            ).first()
            if this_data is None:
                this_data= WeekData(
                    clan_player=clan_player,
                    year=now.isocalendar()[0],
                    week=now.isocalendar()[1]
                )

            last_data = WeekData.query.filter_by(
                clan_player=clan_player,
                year=last_week.isocalendar()[0],
                week=last_week.isocalendar()[1]
            ).first()

            if last_data is None:
                last_data = WeekData(
                    clan_player=clan_player,
                    year=last_week.isocalendar()[0],
                    week=last_week.isocalendar()[1]
                )

            crowns = int(rowdata[row_map["crowns"]].text)
            donations = int(rowdata[row_map["donations"]].text)

            # Sunday and monday until 7:55
            nowmin = (int(now.strftime("%H")) * 60) +  int(now.strftime("%M"))
            is_pre_monday = (int(now.strftime("%w")) == 1
                             and nowmin < cutoff_minute)
            is_post_friday = (
                (int(now.strftime("%w")) > 5 and nowmin > cutoff_minute)
                or int(now.strftime("%w")) == 0
            )

            if is_pre_monday:
                this_data.crowns = 0
                this_data.donations = 0
                last_data.crowns = crowns
                last_data.donations = donations
            elif is_post_friday:
                this_data.crowns = crowns
                this_data.donations = donations
            else:
                this_data.donations = donations
                last_data.crowns = crowns

            db.session.add(this_data)
            db.session.commit()


@app.cli.command()
@click.option('--tag')
@click.option('--name')
def add_clan(tag, name):
    """Create new clan"""
    clan = Clan(clantag=tag, name=name)
    db.init_app(app)
    db.session.add(clan)
    db.session.commit()
