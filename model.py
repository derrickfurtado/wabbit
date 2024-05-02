""" DB seed and models script """

from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

####################### DB Class Models ####################### 


class Users(db.Model):

    __tablename__ = "users_table"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    location = db.Column(db.String(255))
    school = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    headshot = db.Column(db.String(255))

    def __repr__(self):
        return f"ID: {id} -- Name: {self.first_name} {self.last_name}, Email: {self.email}"
    
class Job(db.Model):

    __tablename__ = "job_table"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company_table.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users_table.id"), nullable=False)
    recruiter_id = db.Column(db.Integer, db.ForeignKey("recruiter_table.id"))


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
    last_logged_task = db.Column(db.String(255), nullable=False)
    last_logged_task_time = db.Column(db.DateTime, nullable=False)

    user = db.relationship("Users", backref="job")
    company = db.relationship("Company", backref="job")
    recruiter = db.relationship("Recruiter", backref="job")
    email_task = db.relationship("Email", backref="job")
    call_task = db.relationship("Call", backref="job")
    general_task = db.relationship("General_Task", backref="job")

    def __repr__(self):
        return f"Job ID: {self.id}: {self.title} for company id: {self.company_id}"

class Email(db.Model):

    __tablename__ = "email_table"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_id = db.Column(db.Integer, db.ForeignKey("job_table.id"))
    task_for_id = db.Column(db.Integer, db.ForeignKey("task_employee_index_table.id"))
    due_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    tasks_for = db.relationship("Task_Employee_Index", backref="email")

    def __repr__(self):
        return f"Email ID: {self.id}: attached to Job ID: {self.job_id}"

class Call(db.Model):

    __tablename__ = "call_table"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_id = db.Column(db.Integer, db.ForeignKey("job_table.id"))
    task_for_id = db.Column(db.Integer, db.ForeignKey("task_employee_index_table.id"))
    due_date = db.Column(db.Date, nullable = False)
    description = db.Column(db.String(255))
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Call ID: {self.id}: attached to Job ID: {self.job_id}"

class General_Task(db.Model):

    __tablename__ = "general_task_table"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_id = db.Column(db.Integer, db.ForeignKey("job_table.id"))
    task_for_id = db.Column(db.Integer, db.ForeignKey("task_employee_index_table.id"))
    due_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"General Task ID: {self.id}: attached to Job ID: {self.job_id}"

class Next_Step(db.Model):

    __tablename__ = "next_step_table"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_id = db.Column(db.Integer, db.ForeignKey("job_table.id"), nullable=False)
    task_for_id = db.Column(db.Integer, db.ForeignKey("task_employee_index_table.id"))
    due_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    step_type = db.Column(db.String(255), nullable=False)

    tasks_for = db.relationship("Task_Employee_Index", backref="next_step")

    def __repr__(self):
        return f"Next Step ID: {self.id}: attached to Job ID: {self.job_id}."

class Company(db.Model):

    __tablename__ = "company_table"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    location = db.Column(db.String(255), nullable=False)
    industry = db.Column(db.String(255))
    favorite = db.Column(db.Boolean, default=False)

    recruiter = db.relationship("Recruiter", backref="company")
    employee = db.relationship("Employee", backref="company")

    def __repr__(self):
        return f"Company ID: {self.id} = Name: {self.name} located in {self.location}"

class Task_Employee_Index(db.Model):
    
    __tablename__ = "task_employee_index_table"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employee_table.id"), nullable=False)
    recruiter_id = db.Column(db.Integer, db.ForeignKey("recruiter_table.id"), nullable=False)

    employee = db.relationship("Employee", backref="task_employee_index")
    recruiter = db.relationship("Recruiter", backref="task_employee_index")

    def __repr__(self):
        return f"ID: {self.id} - EmployeeID: {self.employee_id} - RecruiterID: {self.recruiter_id}"

class Recruiter(db.Model):

    __tablename__ = "recruiter_table"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company_table.id"), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    linkedin = db.Column(db.String(255))

    def __repr__(self):
        return f""
    
class Employee(db.Model):

    __tablename__ = "employee_table"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company_table.id"), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    linkedin = db.Column(db.String(255))





def connect_to_db(flask_app, echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = flask_app
    db.init_app(flask_app)

    print("Crank it up to 5432!")


if __name__ == "__main__":
    from server import app
    connect_to_db(app)

    ####################### Seed Scripts ####################### 



