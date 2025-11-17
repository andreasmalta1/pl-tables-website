from flask import Blueprint, render_template, request
from flask_login import current_user

from ...models import Team, Nation, Manager, ManagerStint
from ...utils import update_visits

manager_blueprint = Blueprint("manager", __name__)


@manager_blueprint.route("/current", methods=["GET"])
def current_managers():
    admin = False
    if current_user.is_authenticated:
        admin = True

    update_visits(request.remote_addr, "current_managers", admin)

    if request.method == "GET":
        current_stints = (
            ManagerStint.query.join(Team, ManagerStint.team_id == Team.id)
            .join(Manager, ManagerStint.manager_id == Manager.id)
            .join(Nation, Manager.nation_id == Nation.id)
            .filter(ManagerStint.current == True, Team.current == True)
            .with_entities(
                Team.crest_url.label("crest_url"),
                Manager.name.label("manager_name"),
                Manager.face_url.label("face_url"),
                Nation.flag_url.label("flag_url"),
                ManagerStint.id,
                ManagerStint.date_start,
                ManagerStint.current,
            )
            .all()
        )

        return render_template(
            "blueprints/current_managers.html",
            stints=current_stints,
        )


@manager_blueprint.route("/ended", methods=["GET"])
def old_managers():
    admin = False
    if current_user.is_authenticated:
        admin = True

    update_visits(request.remote_addr, "old_managers", admin)

    if request.method == "GET":
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
                ManagerStint.id,
                ManagerStint.date_start,
                ManagerStint.date_end,
                ManagerStint.current,
            )
            .all()
        )

        return render_template(
            "blueprints/past_managers.html",
            stints=ended_stints,
        )
