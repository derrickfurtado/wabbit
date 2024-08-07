""" DB seed and models script """

from flask_sqlalchemy import SQLAlchemy     ## using SQLAlchemy db
import os, psycopg2                                  ## used to pull in Postgres URI


db = SQLAlchemy()
database_uri = os.environ["DATABASE_URI"]



####################### DB Class Models ####################### 


class Users(db.Model):

    __tablename__ = "users_table"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)            ## changed column data type to be LargeBinary for encryption
    location = db.Column(db.String(255))
    school = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    headshot = db.Column(db.String(255))

    def __repr__(self):
        return f"ID: {id} -- Name: {self.first_name} {self.last_name}, Email: {self.email}"
    
class Job(db.Model):

    __tablename__ = "job_table"                         ## naming tables like this makes it easier to reference them later

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company_table.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users_table.id"), nullable=False)
    recruiter_id = db.Column(db.Integer, db.ForeignKey("recruiter_table.id"))
    referral_id = db.Column(db.Integer, db.ForeignKey("referral_table.id"))

    role = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(4000), nullable=False)
    notes = db.Column(db.String(1000))
    resume = db.Column(db.String(1000))
    requirements = db.Column(db.String(4000), nullable=False)
    salary = db.Column(db.Integer)                              ## nullable in case salary and/or compensation is not present
    compensation = db.Column(db.String(4000))                    
    link = db.Column(db.String(500), nullable=False)
    date_applied = db.Column(db.DateTime)

    job_offer = db.Column(db.Boolean, default=False)            ## boolean for tracking analytics
    rejection = db.Column(db.Boolean, default=False)
    interviewing = db.Column(db.Boolean, default=False)
    accepted_offer = db.Column(db.Boolean, default=False)
    ghosted = db.Column(db.Boolean, default=False)
    favorite = db.Column(db.Boolean, default=False)

    last_logged_task = db.Column(db.String(255))
    last_logged_task_time = db.Column(db.DateTime)

    user = db.relationship("Users", backref="job")                  ## most relationships will be contained on job object
    company = db.relationship("Company", backref="job")
    recruiter = db.relationship("Recruiter", backref="job")
    next_step = db.relationship("Next_Step", backref="job")
    email_task = db.relationship("Email", backref="job")
    call_task = db.relationship("Call", backref="job")
    general_task = db.relationship("General_Task", backref="job")
    referral = db.relationship("Referral", backref="job")

    def __repr__(self):
        return f"Job ID: {self.id}: {self.role} for company id: {self.company_id}"

class Email(db.Model):

    __tablename__ = "email_table"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_id = db.Column(db.Integer, db.ForeignKey("job_table.id"))
    task_for_employee = db.Column(db.Integer, db.ForeignKey("employee_table.id"))       ## haven't implemented this yet for email, calls, or tasks -- May not need it, but it's nullable so it doesn't hurt
    task_for_recruiter = db.Column(db.Integer, db.ForeignKey("recruiter_table.id"))     ## haven't implemented this yet for email, calls, or tasks -- May not need it, but it's nullable so it doesn't hurt
    due_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(500), nullable=False) 
    completed = db.Column(db.Boolean, default=False)

    recruiter = db.relationship("Recruiter", backref="email_task")
    employee = db.relationship("Employee", backref="email_task")

    def __repr__(self):
        return f"Email ID: {self.id}: attached to Job ID: {self.job_id}"

class Call(db.Model):

    __tablename__ = "call_table"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_id = db.Column(db.Integer, db.ForeignKey("job_table.id"))
    task_for_employee = db.Column(db.Integer, db.ForeignKey("employee_table.id"))        ## haven't implemented this yet for email, calls, or tasks -- May not need it, but it's nullable so it doesn't hurt
    task_for_recruiter = db.Column(db.Integer, db.ForeignKey("recruiter_table.id"))      ## haven't implemented this yet for email, calls, or tasks -- May not need it, but it's nullable so it doesn't hurt
    due_date = db.Column(db.Date, nullable = False)
    description = db.Column(db.String(500))
    completed = db.Column(db.Boolean, default=False)

    recruiter = db.relationship("Recruiter", backref="call_task")
    employee = db.relationship("Employee", backref="call_task")

    def __repr__(self):
        return f"Call ID: {self.id}: attached to Job ID: {self.job_id}"

class General_Task(db.Model):

    __tablename__ = "general_task_table"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_id = db.Column(db.Integer, db.ForeignKey("job_table.id"))
    task_for_employee = db.Column(db.Integer, db.ForeignKey("employee_table.id"))        ## haven't implemented this yet for email, calls, or tasks -- May not need it, but it's nullable so it doesn't hurt
    task_for_recruiter = db.Column(db.Integer, db.ForeignKey("recruiter_table.id"))      ## haven't implemented this yet for email, calls, or tasks -- May not need it, but it's nullable so it doesn't hurt
    due_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    recruiter = db.relationship("Recruiter", backref="general_task")
    employee = db.relationship("Employee", backref="general_task")

    def __repr__(self):
        return f"General Task ID: {self.id}: attached to Job ID: {self.job_id}"

class Next_Step(db.Model):

    __tablename__ = "next_step_table"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_id = db.Column(db.Integer, db.ForeignKey("job_table.id"), nullable=False)
    task_for_employee = db.Column(db.Integer, db.ForeignKey("employee_table.id"))       ## this is implemented and critical for rendering the correct next steps
    task_for_recruiter = db.Column(db.Integer, db.ForeignKey("recruiter_table.id"))     ## this is implemented and critical for rendering the correct next steps
    due_date = db.Column(db.Date, nullable=False)
    due_time = db.Column(db.Time, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    step_type = db.Column(db.String(255), nullable=False)


    def __repr__(self):
        return f"Next Step ID: {self.id}: attached to Job ID: {self.job_id}."

class Company(db.Model):

    __tablename__ = "company_table"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    industry = db.Column(db.String(255))
    favorite = db.Column(db.Boolean, default=False)

    recruiter = db.relationship("Recruiter", backref="company")
    employee = db.relationship("Employee", backref="company")

    def __repr__(self):
        return f"Company ID: {self.id} = Name: {self.name} located in {self.location}"

class Recruiter(db.Model):

    __tablename__ = "recruiter_table"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company_table.id"), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    linkedin = db.Column(db.String(255))

    next_step = db.relationship("Next_Step", backref="recruiter")

    def __repr__(self):
        return f"Recruiter name: {self.first_name} {self.last_name}"
    
class Employee(db.Model):

    __tablename__ = "employee_table"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company_table.id"), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    linkedin = db.Column(db.String(255))

    next_step = db.relationship("Next_Step", backref="employee")

    def __repr__(self):
        return f"Employee name: {self.first_name} {self.last_name}"

class Referral(db.Model):

    __tablename__ = "referral_table"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(255), nullable=False)
    linkedin = db.Column(db.String(255))

    def _repr__(self):
        return f"Referral name: {self.full_name}"






def connect_to_db(flask_app, echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URI"]
    # flask_app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]          ### 💡💡💡
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False      ## turned off because the command line feedback was overwhelming
    db.app = flask_app
    db.init_app(flask_app)
    print("Crank it up to 80!")


if __name__ == "__main__":          ## only used if running model.py directly when seeding the DB
    from app import app
    connect_to_db(app)