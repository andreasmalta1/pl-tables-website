from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email


class ContactForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[DataRequired(message="Please enter your name.")],
        render_kw={"placeholder": "Please enter your name"},
    )
    email = StringField(
        "Email",
        validators=[DataRequired(message="Please enter your email address"), Email()], render_kw={"placeholder": "Please enter your email address"}
    )
    subject = StringField(
        "Subject", validators=[DataRequired(message="Please enter a subject.")], render_kw={"placeholder": "Please enter your subject"}
    )
    message = TextAreaField(
        "Message", validators=[DataRequired(message="Please enter a message.")], render_kw={"placeholder": "Please enter your message"}
    )
    submit = SubmitField("Send")
