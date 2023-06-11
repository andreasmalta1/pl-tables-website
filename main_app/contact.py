from flask import Blueprint, render_template, request, flash
from flask_mail import Mail, Message
from os import getenv

from main_app import app
from main_app.forms import ContactForm


contact = Blueprint("contact", __name__)


@contact.route("/contact", methods=["GET", "POST"])
def contact_us():
    """
    Generate the contact us page.
    The POST method, sends an email with the form data
    """
    form = ContactForm()
    if request.method == "POST":
        # Ensure that form data is valid
        if form.validate() == False:
            flash("Enter a valid email address", category="email_contact")
            return render_template("contact.html", form=form)

        # Init Mail class
        mail = Mail()
        mail.init_app(app)

        # Send a message with data collected from form
        msg = Message(
            form.subject.data,
            sender=form.email.data,
            recipients=[getenv("MAIL_USERNAME")],
        )
        msg.body = "From: %s <%s> \n%s" % (
            form.name.data,
            form.email.data,
            form.message.data,
        )
        mail.send(msg)
        return render_template("contact.html")

    if request.method == "GET":
        return render_template("contact.html", form=form)
