from flask import render_template, request

from season import season_blueprint
from models import Match, Season
from utils import update_visits


@season_blueprint.route("/", methods=["GET"])
def seasons():
    # Add page visit to db
    update_visits(request.remote_addr, "seasons")

    if request.method == "GET":
        seasons_query = Match.query.with_entities(Match.season).distinct().all()
        current_season_query = (
            Season.query.with_entities(Season.season).distinct().first()
        )

        seasons = [season.season for season in seasons_query]
        seasons.sort(reverse=True)
        current_season = current_season_query.season

        if current_season in seasons:
            seasons.remove(current_season)

            return render_template(
                "season/seasons.html",
                seasons=seasons,
                current_season=current_season,
            )
