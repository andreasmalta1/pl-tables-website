from flask import Blueprint, render_template, request
from flask_mail import Message
from os import getenv

from ...forms import ContactForm
from ...app import mail

contact_page_blueprint = Blueprint("contact_page", __name__)


@contact_page_blueprint.route("/", methods=["GET", "POST"])
def contact_page():
    """
    Generate the contact us page.
    The POST method, sends an email with the form data
    """
    form = ContactForm()
    if request.method == "GET":
        return render_template("blueprints/contact_page.html", form=form)

    if request.method == "POST":
        # Ensure that form data is valid
        if form.validate() == False:
            message = "Enter a valid email address"
            return render_template(
                "blueprints/contact_page.html", form=form, message=message
            )

        # Send a message with data collected from form
        msg = Message(
            form.subject.data,
            sender=form.email.data,
            recipients=[getenv("MAIL_USERNAME")],
        )
        msg.body = "From: %s <%s> \n%s\n\n\n%s" % (
            form.name.data,
            form.email.data,
            form.message.data,
            "Sent from PL Tables Website",
        )
        mail.send(msg)
        message = "Message sent. I will be in contact with you very soon"
        return render_template(
            "blueprints/contact_page.html", form=form, message=message
        )
