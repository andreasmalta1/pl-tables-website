from flask import render_template, request

from manager import manager_blueprint
from models import Team, Nation, Manager, ManagerStint
from utils import update_visits


@manager_blueprint.route("/", methods=["GET"])
def managers():
    # Add page visit to db
    update_visits(request.remote_addr, "managers")

    if request.method == "GET":
        current_stints = (
            ManagerStint.query.filter_by(current=True)
            .join(Team, ManagerStint.team_id == Team.id)
            .join(Manager, ManagerStint.manager_id == Manager.id)
            .join(Nation, Manager.nation_id == Nation.id)
            .with_entities(
                Team.crest_url.label("crest_url"),
                Manager.name.label("manager_name"),
                Manager.face_url.label("face_url"),
                Nation.flag_url.label("flag_url"),
                ManagerStint.date_start,
                ManagerStint.current,
            )
            .all()
        )

        ended_stints = (
            ManagerStint.query.filter_by(current=False)
            .join(Team, ManagerStint.team_id == Team.id)
            .join(Manager, ManagerStint.manager_id == Manager.id)
            .join(Nation, Manager.nation_id == Nation.id)
            .with_entities(
                Team.crest_url.label("crest_url"),
                Manager.name.label("manager_name"),
                Manager.face_url.label("face_url"),
                Nation.flag_url.label("flag_url"),
                ManagerStint.date_start,
                ManagerStint.date_end,
                ManagerStint.current,
            )
            .all()
        )

        return render_template(
            "manager/managers.html",
            current_stints=current_stints,
            ended_stints=ended_stints,
        )
