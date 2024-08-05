from flask import Blueprint

season_blueprint = Blueprint("season", __name__)


from blueprints.season import routes
