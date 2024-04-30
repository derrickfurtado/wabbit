""" DB seed and models script """

from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


class User(db.Model):

    __tablename__ = "user_table"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255))
    school = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    headshot = db.Column(db.String(255))

    def __repr__(self):
        return f"ID: {id} -- Name: {self.first_name} {self.last_name}, Email: {self.email}"
    
class Job(db.Model):

    __tablename__ = "job_table"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company_table"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user_table"), nullable=False)
    recruiter_id = db.Column(db.Integr, db.ForeignKey("recruiter_table"))
    next_step = db.Column(db.Integer, db.ForeignKey("next_step_table"))

    role = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    requirements = db.Column(db.String(255), nullable=False)
    salary = db.Column(db.Integer)
    compensation = db.Column(db.String(255))
    link = db.Column(db.String(255), nullable=False)
    date_applied = db.Column(db.DateTime, nullable=False)
    job_offer = db.Column(db.Boolean, default=False)
    rejection = db.Column(db.Boolean, default=False)
    declined_offer = db.Column(db.Boolean, default=False)
    accepted_offer = db.Column(db.Boolean, default=False)
    ghosted = db.Column(db.Boolean, default=False)
    favorite = db.Column(db.Boolean, default=False)
    last_looged_task = db.Column(db.String(255), nullable=False)
    last_logged_task_time = db.Column(db.DateTime, nullable=False)

    user = db.relationship("User", backref="job")
    company = db.relationship("Company", backref="job")


class Company(db.Model):

    __tablename__ = "company_table"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    location = db.Column(db.String(255), nullable=False)
    industry = db.Column(db.String(255))

    recruiter = db.relationship("Recruiter", backref="company")
    employee = db.relationship("Company_Team", backref="company")

class Email(db.Model):

    __tablename__ = "email_table"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_id = db.Column(db.Integer, db.ForeignKey("job_table"))
    task_for = db.Column(db.String(255), db.ForeignKey("task_employee_index_table"), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False)

class Call(db.Model):

    __tablename__ = "call_table"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_id = db.Column(db.Integer, db.ForeignKey("job_table"))
    task_for = db.Column(db.String(255))
    due_date = db.Column(db.Date)
    description = db.Column(db.String(255))
    completed = db.Column(db.Boolean, default=False)

class General_Task(db.Model):

    __tablename__ = "general_task_table"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_id = db.Column(db.Integer, db.ForeignKey("job_table"))
    task_for = db.Column(db.String(255), db.ForeignKey("task_employee_index_table"), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False)
