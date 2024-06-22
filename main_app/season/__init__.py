from flask import Blueprint

season_blueprint = Blueprint("season", __name__)


from season import routes
