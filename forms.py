from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, TextAreaField, PasswordField, EmailField, DateField, IntegerField
from wtforms.validators import DataRequired, Length



class User_Login_Form(FlaskForm):
    email = StringField("Email: ", validators=[DataRequired(), Length(min=5, max=255)])
    password = PasswordField("Password: ", validators=[DataRequired(), Length(min=4, max=255)])
    submit = SubmitField("Login")

class User_Registration_Form(FlaskForm):
    first_name = StringField("First Name: ", validators=[DataRequired(), Length(min=2, max=255)])
    last_name = StringField("Last Name: ")
    email = EmailField("Email: ", validators=[DataRequired(), Length(min=5, max=255)])
    password = PasswordField("Password: ", validators=[DataRequired(), Length(min=4, max=255)])
    submit = SubmitField()

class Job_Form(FlaskForm):
    role = StringField("Role Title: ", validators=[DataRequired(), Length(max=255)])
    description = StringField("Job Description: ", validators=(DataRequired(), Length(max=2000)))
    requirements = StringField("Job Requirements: ", validators=[DataRequired(), Length(max=2000)])
    salary = IntegerField("Salary (if present): ")
    compensation = StringField("Other Compensation (if present): ", validators=[Length(max=255)])
    link = StringField("Link to posting: ", validators=[DataRequired(), Length(max=255)])
    company = SelectField("Company: ", coerce=str)              ## coerce allows the form to "look" for a string when invoked
    submit = SubmitField()