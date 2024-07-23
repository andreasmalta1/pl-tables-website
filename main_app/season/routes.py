from flask import render_template, request
from flask_login import current_user

from season import season_blueprint
from models import Match, Season
from utils import update_visits


@season_blueprint.route("/", methods=["GET"])
def seasons():
    admin = False
    if current_user.is_authenticated:
        admin = True

    update_visits(request.remote_addr, "season", admin)

    if request.method == "GET":
        seasons_query = Match.query.with_entities(Match.season).distinct().all()
        current_season_query = (
            Season.query.with_entities(Season.season).distinct().first()
        )

        seasons = [season.season for season in seasons_query]

        current_season = current_season_query.season

        if current_season not in seasons:
            seasons.append(current_season)

        seasons.sort(reverse=True)

        return render_template(
            "season/seasons.html",
            seasons=seasons,
        )
