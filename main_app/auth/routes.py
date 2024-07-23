from flask import render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message
from werkzeug.security import check_password_hash
import os
import datetime

from app import mail
from auth import auth_blueprint
from models import User


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect(url_for("home.index"))

        return render_template("auth/login.html")

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()

        msg = Message(
            "Login Attempt",
            sender=os.getenv("MAIL_USERNAME"),
            recipients=[os.getenv("MAIL_USERNAME")],
        )
        msg.body = "Login Attempt\nEmail: %s\nTimeStamp: %s\nIP Address: %s" % (
            email,
            datetime.datetime.now(),
            request.remote_addr,
        )
        mail.send(msg)

        if not user or not check_password_hash(user.password, password):
            return render_template("auth/login.html")

        login_user(user, remember=False)
        return redirect(url_for("home.index"))


@auth_blueprint.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("home.index"))
