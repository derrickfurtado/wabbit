from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, PasswordField, EmailField, DateField, IntegerField, TimeField
from wtforms.validators import DataRequired, Length



class User_Login_Form(FlaskForm):
    eml = StringField("Email: ", validators=[DataRequired(), Length(min=5, max=255)])
    pwd = PasswordField("Password: ", validators=[DataRequired(), Length(min=4, max=255)])
    sbmt = SubmitField("Login")

class User_Registration_Form(FlaskForm):
    first_name = StringField("First Name: ", validators=[DataRequired(), Length(min=2, max=255)])
    last_name = StringField("Last Name: ")
    email = EmailField("Email: ", validators=[DataRequired(), Length(min=5, max=255)])
    password = PasswordField("Password: ", validators=[DataRequired(), Length(min=4, max=255)])
    submit = SubmitField()

class Job_Form(FlaskForm):
    role = StringField("Role Title: ", validators=[DataRequired(), Length(max=255)])
    description = TextAreaField("Job Description: ", validators=(DataRequired(), Length(max=4000)))
    requirements = TextAreaField("Job Requirements: ", validators=[DataRequired(), Length(max=4000)])
    salary = IntegerField("Salary (if present): ")
    compensation = TextAreaField("Other Compensation (if present): ", validators=[Length(max=4000)])
    link = StringField("Link to posting: ", validators=[DataRequired(), Length(max=500)])
    company = SelectField("Company: ", coerce=str)              ## coerce allows the form to "look" for a string when invoked
    submit = SubmitField()

class Notes_Form(FlaskForm):
    link = StringField("Link to Google Notes: ", validators=[Length(max=1000)])
    submit = SubmitField("Attach Notes Here")

class Resume_Form(FlaskForm):
    link = StringField("Link to Resume: ", validators=[Length(max=1000)])
    submit = SubmitField("Attach Resume Link Here")

class Company_Form(FlaskForm):
    name = StringField("Company Name: ", validators=[DataRequired(), Length(max=255)])
    location = StringField("Location: ", validators=[DataRequired(), Length(max=255)])
    industry = StringField("Industry: ", validators=[Length(max=255)])
    submit = SubmitField()

class Employee_Form(FlaskForm):
    first_name = StringField("First Name: ", validators=[DataRequired(), Length(max=255)])
    last_name = StringField("Last Name: ", validators=[Length(max=255)])
    title = StringField("Title: ", validators=[DataRequired(), Length(max=255)])
    email = EmailField("Email: ", validators=[Length(max=255)])
    linkedin = StringField("LinkedIn page: ", validators=[Length(max=255)])
    submit = SubmitField()

class Recruiter_Form(FlaskForm):
    first_name = StringField("First Name: ", validators=[DataRequired(), Length(max=255)])
    last_name = StringField("Last Name: ", validators=[Length(max=255)])
    title = StringField("Title: ", validators=[DataRequired(), Length(max=255)])
    email = EmailField("Email: ", validators=[Length(max=255)])
    linkedin = StringField("LinkedIn page: ", validators=[Length(max=255)])
    submit = SubmitField()

class Update_Email_Form(FlaskForm):
    email = StringField("Email Address: ", validators=[Length(max=255)])
    submit = SubmitField()

class Update_Salary_Form(FlaskForm):
    salary = IntegerField("Updated Salary: ")
    submit = SubmitField()

class Referral_Form(FlaskForm):
    full_name = StringField("Full Name: ", validators=[DataRequired(), Length(max=255)])
    linkedin = StringField("LinkedIn: ", validators=[Length(max=255)])
    submit = SubmitField()

class SNE_Recruiter_Form(FlaskForm):        ## used coerce to make step types dynamic
    task_for_recruiter_id = SelectField("Which recruiter? ", coerce=str)
    due_date = DateField("Date of Event: ", validators=[DataRequired()])
    due_time = TimeField("Time of Event: ", validators=[DataRequired()])
    description = TextAreaField("Description: ", validators=[DataRequired(), Length(max=255)])
    step_type = SelectField("Type of Call", coerce=str)                                             ## coerce=str helped to make the list options dynamic in server.py 
    submit = SubmitField()

class SNE_Employee_Form(FlaskForm):
    task_for_employee_id = SelectField("Which employee?", coerce=str)
    due_date = DateField("Date of Event:", validators=[DataRequired()])
    due_time = TimeField("Time of Event: ", validators=[DataRequired()])
    description = TextAreaField("Description: ", validators=[DataRequired(), Length(max=255)])
    step_type = SelectField("Type of Call", coerce=str)
    submit = SubmitField()

class Call_Form(FlaskForm):
    due_date = DateField("When are you making this call? ", validators=[DataRequired()])
    description = TextAreaField("Describe the goal of the call: ", validators=[Length(max=500)])
    submit = SubmitField()

class Email_Form(FlaskForm):
    due_date = DateField("When are you sending this email? ", validators=[DataRequired()])
    description = TextAreaField("Describe the goal of the email: ", validators=[Length(max=500)])
    submit = SubmitField()

class General_Task_Form(FlaskForm):
    due_date = DateField("When should this task be completed? ", validators=[DataRequired()])
    description = TextAreaField("Describe the task: ", validators=[Length(max=500)])
    submit = SubmitField()