from main_app import db
from sqlalchemy.sql import func


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    home_team = db.Column(db.String(100), unique=False)
    away_team = db.Column(db.String(100), unique=False)
    home_score = db.Column(db.Integer(), default=0)
    away_score = db.Column(db.Integer(), default=0)
    date = db.Column(db.Date(), default=func.now())
    season = db.Column(db.String(9), unique=False)
    date_added = db.Column(db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return f"{self.home_team} {self.home_score} - {self.away_score} {self.away_team}"
