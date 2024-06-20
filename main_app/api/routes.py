from flask import jsonify

from api import api_blueprint


@api_blueprint.route("/matches", methods=["GET"])
def matches():
    return jsonify({"match": "match"})
