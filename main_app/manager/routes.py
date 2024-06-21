from flask import jsonify, render_template, request
from datetime import date, datetime
from sqlalchemy.orm import joinedload

from manager import manager_blueprint
from models import Team, Nation, Manager, ManagerStint
from utils import generate_table, update_visits


@manager_blueprint.route("/", methods=["GET"])
def managers():
    """
    Managers route
    The GET method displays are hardcoded list of mangers and ther times in charge
    The POST method reroutes to the custom page and shows the table for the time in charge for the chosen manager
    """

    # Add page visit to db
    update_visits(request.remote_addr, "managers")

    if request.method == "GET":
        stints = (
            ManagerStint.query.join(Team, ManagerStint.team_id == Team.id)
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
            "manager/managers_test.html",
            managers=stints,
        )

        # Example of processing the query results
        for result in stints:
            print(
                f"Team: {result.team_name}, Manager: {result.manager_name}, Nation: {result.nation_name}, Start Date: {result.date_start}"
            )

        # Get today's date
        date_today = date.today()

        for manager_id in managers_dict:
            if managers_dict[manager_id]["status"] == "current":
                current_managers[manager_id] = managers_dict[manager_id]
                # Get the managers start date and calculate number of day's in charge
                date_start = current_managers[manager_id]["date_start"].split("-")
                d0 = date(int(date_start[0]), int(date_start[1]), int(date_start[2]))
                delta = date_today - d0

                current_managers[manager_id]["days_in_charge"] = delta.days
                current_managers[manager_id][
                    "manager_url"
                ] = f"{MANAGER_FACE_URL}{current_managers[manager_id]['fotmob_id']}.png"
                current_managers[manager_id][
                    "nationality_url"
                ] = f"{CREST_URL}{NATIONS.get(current_managers[manager_id]['nationality'])}.png"
                current_managers[manager_id][
                    "club_url"
                ] = f"{CREST_URL}{TEAMS.get(current_managers[manager_id]['club'])['logo_id']}.png"

            if managers_dict[manager_id]["status"] == "memorable":
                memorable_managers[manager_id] = managers_dict[manager_id]
                # Get manager's start date
                date_start = memorable_managers[manager_id]["date_start"].split("-")
                date_end = memorable_managers[manager_id]["date_end"]
                # Get managers end day even if manager is still active
                if date_end == "today":
                    date_end = date_today
                    memorable_managers[manager_id]["date_end"] = datetime.strftime(
                        date_today, "%Y-%m-%d"
                    )
                else:
                    date_end = date_end.split("-")
                    date_end = date(
                        int(date_end[0]), int(date_end[1]), int(date_end[2])
                    )

                d0 = date(int(date_start[0]), int(date_start[1]), int(date_start[2]))
                delta = date_end - d0

                memorable_managers[manager_id]["days_in_charge"] = delta.days
                if memorable_managers[manager_id]["fotmob_id"]:
                    memorable_managers[manager_id][
                        "manager_url"
                    ] = f"{MANAGER_FACE_URL}{memorable_managers[manager_id]['fotmob_id']}.png"
                else:
                    memorable_managers[manager_id]["manager_url"] = f"{EMPTY_FACE_URL}"

                memorable_managers[manager_id][
                    "nationality_url"
                ] = f"{CREST_URL}{NATIONS.get(memorable_managers[manager_id]['nationality'])}.png"
                memorable_managers[manager_id][
                    "club_url"
                ] = f"{CREST_URL}{TEAMS.get(memorable_managers[manager_id]['club'])['logo_id']}.png"

        # Sort managers by days in charge
        sorted_current_managers = sorted(
            current_managers.items(),
            key=lambda x: x[1]["days_in_charge"],
            reverse=True,
        )
        sorted_current_managers = dict(sorted_current_managers)

        sorted_memorable_managers = sorted(
            memorable_managers.items(),
            key=lambda x: x[1]["days_in_charge"],
            reverse=True,
        )
        sorted_memorable_managers = dict(sorted_memorable_managers)

        return render_template(
            "managers.html",
            current_managers=sorted_current_managers,
            memorable_managers=sorted_memorable_managers,
        )
