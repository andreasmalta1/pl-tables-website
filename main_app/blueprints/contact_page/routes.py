from flask import render_template, request, flash
from flask_mail import Message
from os import getenv

from forms import ContactForm
from app import mail

from blueprints.contact_page import contact_page_blueprint


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
            flash("Enter a valid email address", category="email_contact")
            return render_template("blueprints/contact_page.html", form=form)

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
        return render_template("blueprints/contact_page.html")
