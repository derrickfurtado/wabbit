from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length


class User_Login_Form(FlaskForm):
    email = StringField("Email: ", validators=[DataRequired(), Length(min=5, max=255)])
    password = PasswordField("Password: ", validators=[DataRequired(), Length(min=4, max=255)])
    submit = SubmitField("Login")

class User_Registration_Form(FlaskForm):
    first_name = StringField("First Name: ", validators=[DataRequired(), Length(min=2, max=255)])
    last_name = StringField("Last Name: ")
    email = StringField("Email: ", validators=[DataRequired(), Length(min=5, max=255)])
    password = PasswordField("Password: ", validators=[DataRequired(), Length(min=4, max=255)])
    submit = SubmitField()