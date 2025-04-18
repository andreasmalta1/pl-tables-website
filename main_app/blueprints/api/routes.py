from flask import Blueprint, jsonify, request
from sqlalchemy.orm import aliased
from datetime import date, datetime
import os
import io
import base64
import pandas as pd
import matplotlib
import urllib.request
from PIL import Image

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from ...models import *
from ...utils import generate_table

api_blueprint = Blueprint("api", __name__)


@api_blueprint.route("/current-season", methods=["GET"])
def index():
    season = Season.query.first().season
    standings_dict = get_matches_by_season(season)
    return jsonify(standings_dict)


@api_blueprint.route("/all-time", methods=["GET"])
def get_all_time():
    standings_dict = get_matches_by_season(season=None)
    return jsonify(standings_dict)


@api_blueprint.route("/seasons/<season>", methods=["GET"])
def seasons(season):
    season = season.replace("-", "/")
    standings_dict = get_matches_by_season(season)
    return jsonify(standings_dict)


@api_blueprint.route("/stints/<int:stint_id>", methods=["GET"])
def stints(stint_id):
    manager_stint = ManagerStint.query.filter_by(id=stint_id).first()
    date_start = manager_stint.date_start
    if manager_stint.current:
        date_end = date.today()
    if not manager_stint.current:
        date_end = manager_stint.date_end

    standings_dict = get_matches_by_day(date_start, date_end)
    return jsonify(standings_dict)


@api_blueprint.route("/managers/<int:stint_id>", methods=["GET"])
def managers(stint_id):
    ManagerTable = aliased(Manager, name="manager_table")
    NationTable = aliased(Nation, name="nation_table")
    TeamTable = aliased(Team, name="team_table")

    manager_query = (
        ManagerStint.query.filter_by(id=stint_id)
        .join(ManagerTable, ManagerTable.id == ManagerStint.manager_id)
        .join(NationTable, NationTable.id == ManagerTable.nation_id)
        .join(TeamTable, TeamTable.id == ManagerStint.team_id)
        .add_columns(
            ManagerStint.date_start,
            ManagerStint.date_end,
            ManagerTable.name.label("manager_name"),
            ManagerTable.face_url.label("manager_face_url"),
            NationTable.name.label("nation_name"),
            NationTable.flag_url.label("nation_flag_url"),
            TeamTable.name.label("team_name"),
            TeamTable.crest_url.label("team_crest_url"),
        )
        .first()
    )

    manager_info = {
        "name": manager_query.manager_name,
        "face_url": manager_query.manager_face_url,
        "date_start": manager_query.date_start.strftime("%Y-%m-%d"),
        "date_end": (
            None
            if not manager_query.date_end
            else manager_query.date_end.strftime("%Y-%m-%d")
        ),
        "team_name": manager_query.team_name,
        "team_crest_url": manager_query.team_crest_url,
        "nation_name": manager_query.nation_name,
        "nation_flag_url": manager_query.nation_flag_url,
    }

    return jsonify(manager_info)


@api_blueprint.route("/dates/<date_start>/<date_end>", methods=["GET"])
def dates(date_start, date_end):
    standings_dict = get_matches_by_day(date_start, date_end)
    return jsonify(standings_dict)


@api_blueprint.route("/years/<int:year>", methods=["GET"])
def calendar_year(year):
    date_start = date(year, 1, 1)
    date_end = date(year, 12, 31)
    standings_dict = get_matches_by_day(date_start, date_end)
    return jsonify(standings_dict)


@api_blueprint.route("/deductions/<season>", methods=["GET"])
def point_deductions(season):
    if season == "current":
        season = Season.query.first().season

    season = season.replace("-", "/")
    TeamTable = aliased(Team, name="team_table")
    points_deductions = (
        PointDeduction.query.filter_by(season=season)
        .join(TeamTable, TeamTable.id == PointDeduction.team_id)
        .add_columns(
            PointDeduction.id,
            PointDeduction.points_deducted,
            PointDeduction.reason,
            PointDeduction.season,
            TeamTable.name.label("team_name"),
        )
        .all()
    )

    if len(points_deductions) == 0:
        return jsonify({})

    deductions_dict = {}
    for deduction in points_deductions:
        deductions_dict[deduction.id] = {
            "team_name": deduction.team_name,
            "reason": deduction.reason,
            "points_deducted": deduction.points_deducted,
        }
    return jsonify(deductions_dict)


@api_blueprint.route("/get-current-season", methods=["GET"])
def get_current_season():
    season = Season.query.first().season

    return jsonify({"season": season})


@api_blueprint.route("/download-table", methods=["POST"])
def download_table():
    dataObj = request.json.get("tableDataObj")
    table = dataObj.get("tableData")
    title = dataObj.get("title")
    deductions = dataObj.get("deductions")
    manager_face = dataObj.get("managerFace")
    team_logo = dataObj.get("teamLogo")
    nation_logo = dataObj.get("nationLogo")
    highlight_team = dataObj.get("teamName")
    highlight_color = "#FFD700"

    df = pd.DataFrame(table)

    image_path = os.path.join(os.getcwd(), "main_app", "static", "images", "pl.png")
    bg_img = mpimg.imread(image_path)

    aspect_ratio = 1.0
    table_length = len(table)
    if deductions:
        table_length += len(deductions)

    fig_height = table_length * 0.5 + 2
    fig_width = fig_height * aspect_ratio
    if fig_width > 20:
        fig_width = fig_width * 0.75

    fig = plt.figure(figsize=(fig_width, fig_height), dpi=300, facecolor="#EFE9E6")
    ax = plt.subplot()

    ncols = 12
    nrows = df.shape[0]

    ax.set_xlim(0, ncols + 1)
    ax.set_ylim(0, nrows + 1)

    positions = [0.05, 1, 2, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5]
    columns = ["#", "", "Team", "MP", "W", "D", "L", "GF", "GA", "GD", "PTS"]

    for i in range(nrows):
        if highlight_team:
            team_name = df["Team"].iloc[i]
            if team_name == highlight_team:
                ax.add_patch(
                    plt.Rectangle(
                        (0, nrows - i - 1),
                        ncols + 1,
                        1,
                        color=highlight_color,
                        alpha=0.3,
                        zorder=1,
                    )
                )

        for j, column in enumerate(columns):
            fontsize = 10

            if not column:
                continue

            text_label = f"{df[column].iloc[i]}"
            weight = "normal"

            ax.annotate(
                xy=(positions[j], nrows - i - 0.5),
                text=text_label,
                ha="center",
                va="center",
                weight=weight,
                fontsize=fontsize,
            )

    DC_to_FC = ax.transData.transform
    FC_to_NFC = fig.transFigure.inverted().transform

    DC_to_NFC = lambda x: FC_to_NFC(DC_to_FC(x))

    ax_point_1 = DC_to_NFC([5.75, 0.25])
    ax_point_2 = DC_to_NFC([6.25, 0.75])
    ax_width = abs(ax_point_1[0] - ax_point_2[0])
    ax_height = abs(ax_point_1[1] - ax_point_2[1]) * 1.2

    for x in range(0, nrows):
        pos = nrows - x - 1
        ax_coords = DC_to_NFC([4, x + 0.25])
        flag_ax = fig.add_axes([ax_coords[0], ax_coords[1], ax_width, ax_height])
        show_logo(df[""].iloc[pos], flag_ax)

    ax_point_1 = DC_to_NFC([4, 0.05])
    ax_point_2 = DC_to_NFC([5, 0.95])
    ax_width = abs(ax_point_1[0] - ax_point_2[0])
    ax_height = abs(ax_point_1[1] - ax_point_2[1])

    for index, _ in enumerate(columns):
        ax.annotate(
            xy=(positions[index], nrows + 0.25),
            text=columns[index],
            ha="center",
            va="bottom",
            weight="bold",
        )

    ax.plot(
        [ax.get_xlim()[0], ax.get_xlim()[1]],
        [nrows, nrows],
        lw=1.5,
        color="black",
        marker="",
        zorder=4,
    )
    ax.plot(
        [ax.get_xlim()[0], ax.get_xlim()[1]],
        [0, 0],
        lw=1.5,
        color="black",
        marker="",
        zorder=4,
    )

    for x in range(1, nrows):
        ax.plot(
            [ax.get_xlim()[0], ax.get_xlim()[1]],
            [x, x],
            lw=1.15,
            color="gray",
            ls=":",
            zorder=3,
            marker="",
        )

    ax.set_axis_off()

    title_location = 0.88
    title_size = 14

    if manager_face and nation_logo and team_logo and highlight_team:
        face_ax = fig.add_axes([0.15, 0.89, 0.05, 0.05])
        team_ax = fig.add_axes([0.22, 0.89, 0.05, 0.05])
        nation_ax = fig.add_axes([0.80, 0.89, 0.05, 0.05])

        face = Image.open(urllib.request.urlopen(manager_face))
        team = Image.open(urllib.request.urlopen(team_logo))
        nation = Image.open(urllib.request.urlopen(nation_logo))

        face_ax.imshow(face, alpha=1)
        face_ax.axis("off")

        team_ax.imshow(team, alpha=1)
        team_ax.axis("off")

        nation_ax.imshow(nation, alpha=1)
        nation_ax.axis("off")

        title_location = 0.90
        title_size = 18

    fig.text(
        x=0.5,
        y=title_location,
        s=title,
        ha="center",
        va="bottom",
        weight="bold",
        size=title_size,
    )

    ax_place = -5

    if deductions:
        for deduction in deductions:
            ax.annotate(
                deduction,
                (0, 0),
                (0, ax_place),
                fontsize=11,
                xycoords="axes fraction",
                textcoords="offset points",
                va="top",
            )

            ax_place -= 25

    ax.annotate(
        f"Generated on {datetime.today().strftime('%Y-%m-%d')}",
        (0, 0),
        (0, ax_place),
        fontsize=10,
        xycoords="axes fraction",
        textcoords="offset points",
        va="top",
    )

    ax_place -= 20

    ax.annotate(
        "Downloaded from pl-tables.com",
        (0, 0),
        (0, ax_place),
        fontsize=10,
        xycoords="axes fraction",
        textcoords="offset points",
        va="top",
    )

    ax.set_xlim(0, ncols + 1)
    ax.set_ylim(0, nrows + 1)
    ax.imshow(
        bg_img, extent=[0, ncols + 1, 0, nrows + 1], aspect="auto", alpha=0.3, zorder=-1
    )

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=300)
    plt.close(fig)
    buf.seek(0)

    img_str = base64.b64encode(buf.getvalue()).decode("utf-8")

    return jsonify({"image": img_str})


def get_matches_by_season(season=None):
    HomeTeam = aliased(Team, name="home_team")
    AwayTeam = aliased(Team, name="away_team")

    if season:
        matches = (
            Match.query.filter_by(season=season)
            .join(HomeTeam, HomeTeam.id == Match.home_team_id)
            .join(AwayTeam, AwayTeam.id == Match.away_team_id)
            .add_columns(
                HomeTeam.name.label("home_team_name"),
                Match.home_score,
                AwayTeam.name.label("away_team_name"),
                Match.away_score,
            )
            .all()
        )

    if not season:
        matches = (
            Match.query.join(HomeTeam, HomeTeam.id == Match.home_team_id)
            .join(AwayTeam, AwayTeam.id == Match.away_team_id)
            .add_columns(
                HomeTeam.name.label("home_team_name"),
                Match.home_score,
                AwayTeam.name.label("away_team_name"),
                Match.away_score,
            )
            .all()
        )

    standings = generate_table(matches, season)
    standings_dict = {}
    for team in standings:
        standings_dict[team[0]] = team[1]

    return standings_dict


def get_matches_by_day(date_start, date_end):
    HomeTeam = aliased(Team, name="home_team")
    AwayTeam = aliased(Team, name="away_team")

    matches = (
        Match.query.filter(db.and_(Match.date >= date_start, Match.date <= date_end))
        .join(HomeTeam, HomeTeam.id == Match.home_team_id)
        .join(AwayTeam, AwayTeam.id == Match.away_team_id)
        .add_columns(
            HomeTeam.name.label("home_team_name"),
            Match.home_score,
            AwayTeam.name.label("away_team_name"),
            Match.away_score,
        )
        .all()
    )

    standings = generate_table(matches, None)
    standings_dict = {}
    for team in standings:
        standings_dict[team[0]] = team[1]

    return standings_dict


def show_logo(url, ax):
    icon = Image.open(urllib.request.urlopen(url))
    ax.imshow(icon, alpha=1)
    ax.axis("off")
    return ax
