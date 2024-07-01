from flask_login import UserMixin
from sqlalchemy.sql import func


from app import db


class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)
    shortcode = db.Column(db.String(5), unique=True, nullable=False)
    crest_url = db.Column(db.String(100), unique=False)
    current = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        """Return the string representing a team."""
        return self.name


class Match(db.Model):
    __tablename__ = "matches"

    id = db.Column(db.Integer(), primary_key=True)
    home_team_id = db.Column(
        db.Integer, db.ForeignKey("teams.id"), unique=False, nullable=False
    )
    away_team_id = db.Column(
        db.Integer, db.ForeignKey("teams.id"), unique=False, nullable=False
    )
    home_score = db.Column(db.Integer(), server_default="0")
    away_score = db.Column(db.Integer(), server_default="0")
    date = db.Column(db.Date(), server_default=func.now())
    season = db.Column(db.String(9), unique=False)
    date_added = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        """Return the string representing a match."""
        return f"{self.home_team_id} {self.home_score} - {self.away_score} {self.away_team_id}"


class Nation(db.Model):
    __tablename__ = "nations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)
    shortcode = db.Column(db.String(5), unique=True, nullable=False)
    flag_url = db.Column(db.String(100), unique=False)

    def __repr__(self):
        """Return the string representing a nation."""
        return self.name


class Manager(db.Model):
    __tablename__ = "managers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)
    face_url = db.Column(db.String(100), unique=False)
    nation_id = db.Column(
        db.Integer, db.ForeignKey("nations.id"), unique=False, nullable=False
    )

    def __repr__(self):
        """Return the string representing a manager."""
        return self.name


class ManagerStint(db.Model):
    __tablename__ = "managerstints"

    id = db.Column(db.Integer, primary_key=True)
    manager_id = db.Column(
        db.Integer, db.ForeignKey("managers.id"), unique=False, nullable=False
    )
    team_id = db.Column(
        db.Integer, db.ForeignKey("teams.id"), unique=False, nullable=False
    )
    date_start = db.Column(db.Date(), nullable=False)
    date_end = db.Column(db.Date(), nullable=True)
    current = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        """Return the string representing a managerial stint."""
        return f"{self.manager_id} - {self.team_id}"


class PointDeduction(db.Model):
    __tablename__ = "pointdeductions"

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(
        db.Integer, db.ForeignKey("teams.id"), unique=False, nullable=False
    )
    points_deducted = db.Column(db.Integer(), unique=False)
    reason = db.Column(db.Text(), unique=False)
    season = db.Column(db.String(9), unique=False)

    def __repr__(self):
        """Return the string representing a match."""
        return f"{self.team_id} - {self.reason} - {self.season}"


class Season(db.Model):
    __tablename__ = "season"

    id = db.Column(db.Integer, primary_key=True)
    season = db.Column(db.String(9), unique=False)

    def __repr__(self):
        """Return the string representing a season."""
        return "Season: {}".format(self.season)


class Visit(db.Model):
    __tablename__ = "visits"

    id = db.Column(db.Integer, primary_key=True)
    user_ip = db.Column(db.String(15), unique=False)
    page_name = db.Column(db.String(25))

    def __repr__(self):
        """Return the string representing a visit."""
        return "Page: {}".format(self.page_name)

    def update_visits(self, user_ip, pagename):
        """Add a visit to the database"""
        self.user_ip, self.page_name = user_ip, pagename
        db.session.add(self)
        db.session.commit()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

    def __repr__(self):
        """Return the string representing a visit."""
        return self.name
