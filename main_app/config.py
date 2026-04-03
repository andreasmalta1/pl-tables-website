import os
import redis
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_TYPE = os.environ.get("SESSION_TYPE")
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url(os.environ.get("REDIS_URL"))

    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True

    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT"))
    MAIL_USE_SSL = bool(int(os.environ.get("MAIL_USE_SSL")))
    MAIL_USE_TLS = bool(int(os.environ.get("MAIL_USE_TLS")))
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
