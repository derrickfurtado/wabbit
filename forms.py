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

class Company_Form(FlaskForm):
    name = StringField("Company Name: ", validators=[DataRequired(), Length(max=255)])
    location = StringField("Location: ", validators=[DataRequired(), Length(max=255)])
    industry = StringField("Industry: ", validators=[Length(max=255)])
    submit = SubmitField()

class Employee_Form(FlaskForm):
    first_name = StringField("First Name: ", validators=[DataRequired(), Length(max=255)])
    last_name = StringField("Last Name: ", validators=[Length(max=255)])
    title = StringField("Title: ", validators=[DataRequired(), Length(max=255)])
    email = EmailField("Email", validators=[DataRequired(), Length(max=255)])
    linkedin = StringField("LinkedIn page: ", validators=[Length(max=255)])
    submit = SubmitField()

class Recruiter_Form(FlaskForm):
    first_name = StringField("First Name: ", validators=[DataRequired(), Length(max=255)])
    last_name = StringField("Last Name: ", validators=[Length(max=255)])
    title = StringField("Title: ", validators=[DataRequired(), Length(max=255)])
    email = EmailField("Email", validators=[DataRequired(), Length(max=255)])
    linkedin = StringField("LinkedIn page: ", validators=[Length(max=255)])
    submit = SubmitField()

class SNE_Recruiter_Form(FlaskForm):
    task_for_recruiter_id = SelectField("Which recruiter? ", coerce=str)
    due_date = DateField("Due Date or Date of Event:", validators=[DataRequired()])
    description = StringField("Description: ", validators=[DataRequired(), Length(max=255)])
    step_type = StringField("Next Step Category", validators=[DataRequired(), Length(max=255)])
    submit = SubmitField()

class SNE_Employee_Form(FlaskForm):
    task_for_employee_id = SelectField("Which employee?", coerce=str)
    due_date = DateField("Due Date or Date of Event:", validators=[DataRequired()])
    description = StringField("Description: ", validators=[DataRequired(), Length(max=255)])
    step_type = StringField("Next Step Category", validators=[DataRequired(), Length(max=255)])
    submit = SubmitField()




