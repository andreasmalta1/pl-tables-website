from flask import Blueprint, render_template, request

from ...models import Match, Season

season_blueprint = Blueprint("season", __name__)


@season_blueprint.route("/", methods=["GET"])
def seasons():
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
            "blueprints/seasons.html",
            seasons=seasons,
        )
