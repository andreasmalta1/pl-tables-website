from main_app import db
from sqlalchemy.sql import func


class Teams(db.Model):
    name = db.Column(db.String(100), unique=False)
    crest_url = db.Column(db.String(100), unique=False)

    def __repr__(self):
        """Return the string representing a match."""
        return self.team_name


class Match(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    # home_team relationship
    # away_team relationship
    home_score = db.Column(db.Integer(), server_default="0")
    away_score = db.Column(db.Integer(), server_default="0")
    date = db.Column(db.Date(), server_default=func.now())
    season = db.Column(db.String(9), unique=False)
    date_added = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        """Return the string representing a match."""
        return f"{self.home_team_name} {self.home_score} - {self.away_score} {self.away_team_name}"


class Nations(db.Model):
    name = db.Column(db.String(100), unique=False)
    flag_url = db.Column(db.String(100), unique=False)

    def __repr__(self):
        """Return the string representing a match."""
        return self.team_name


class Managers(db.Model):
    name = db.Column(db.String(100), unique=False)
    face_url = db.Column(db.String(100), unique=False)
    # nation relationship

    def __repr__(self):
        """Return the string representing a match."""
        return self.team_name


class ManagerStints(db.Model):
    # manager relationship
    # club relationship
    date_start = db.Column(db.Date(), nullable=False)
    date_end = db.Column(db.Date(), nullable=True)
    current = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        """Return the string representing a match."""
        return self.team_name


class PointDeductions(db.Model):
    # team_relationship
    points_deducted = db.Column(db.Integer(), unique=False)
    reason = db.Column(db.Text(), unique=False)
    season = db.Column(db.String(9), unique=False)

    def __repr__(self):
        """Return the string representing a match."""
        return self.team_name


class Visit(db.Model):
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
