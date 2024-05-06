""" Seed file to create/delete DB and add test data to our Wabbit DB for testing/building only"""

import os, model, server, json, crud
from pdb import set_trace

server.app.app_context().push()

os.system("dropdb wabbit")              ## drop table and all data
os.system("createdb wabbit")            ## recreate table

model.connect_to_db(server.app)         ## connect to Wabbit DB
model.db.create_all()                   ## create all tables

with open ('data/test_data.json') as file:  ## open and read .json file
    test_data = json.loads(file.read())     ## test_data will be a list of dictionaries for each dataclass object



### Create Company test data ###
company_data = test_data[6]["company"]
name = company_data["name"]
location = company_data["location"]
industry = company_data["industry"]
favorite = eval(company_data["favorite"])

test_company = crud.create_company(name, location, industry, favorite)
model.db.session.add(test_company)
model.db.session.commit()


### Create User Test Data ###
user_data = test_data[0]["users"]           ## each dataclass object has a specific index
first_name = user_data["first_name"]
last_name = user_data["last_name"]
email = user_data["email"]
password = user_data["password"]
location = user_data["location"]
school = user_data["school"]
bio = user_data["bio"]
headshot = user_data["headshot"]
test_user = crud.create_user(first_name, last_name, email, password, location, school, bio, headshot)

model.db.session.add(test_user)
model.db.session.commit()


### Create Job Test Data ###
job_data = test_data[1]["job"]
company_id = job_data["company_id"]
user_id = job_data["user_id"]
role = job_data["role"]
description = job_data["description"]
requirements = job_data["requirements"]
salary = job_data["salary"]
compensation = job_data["compensation"]
link = job_data["link"]
date_applied = job_data["date_applied"]
job_offer = eval(job_data["job_offer"])
rejection = eval(job_data["rejection"])
declined_offer = eval(job_data["declined_offer"])
accepted_offer = eval(job_data["accepted_offer"])
ghosted = eval(job_data["ghosted"])
favorite = eval(job_data["favorite"])
last_logged_task = job_data["last_logged_task"]
last_logged_task_time = job_data["last_logged_task_time"]

test_job = crud.create_job(company_id, user_id, None, role, description, requirements, salary, compensation, link, date_applied, job_offer, rejection, declined_offer, accepted_offer, ghosted, favorite, last_logged_task, last_logged_task_time)            ### added None to certain fields that required dependencies. Only needed upon creation of test data

model.db.session.add(test_job)
model.db.session.commit()

###  Create Next Step test data ###
next_step_data = test_data[5]["next_step"]
job_id = next_step_data["job_id"]
due_date = next_step_data["due_date"]
description = next_step_data["description"]
step_type = next_step_data["step_type"]

test_next_step = crud.create_next_step(job_id, None, due_date, description, step_type)
model.db.session.add(test_next_step)
model.db.session.commit()


### Create Email test data ###
email_data = test_data[2]["email"]
job_id = email_data["job_id"]
due_date = email_data["due_date"]
description = email_data["description"]
completed = eval(email_data["completed"])

test_email = crud.create_email(job_id, None, due_date, description, completed)
model.db.session.add(test_email)
model.db.session.commit()


### Create Call test data ###
call_data = test_data[3]["call"]
job_id = call_data["job_id"]
due_date = call_data["due_date"]
description = call_data["description"]
completed = eval(call_data["completed"])

test_call = crud.create_call(job_id, None, due_date, description, completed)
model.db.session.add(test_call)
model.db.session.commit()


### Create General Task data ###
general_task_data = test_data[4]["general_task"]
job_id = general_task_data["job_id"]
due_date = general_task_data["due_date"]
description = general_task_data["description"]
completed = eval(general_task_data["completed"])

test_general_task = crud.create_general_task(job_id, None, due_date, description, completed)
model.db.session.add(test_general_task)
model.db.session.commit()




### Create Recruiter test data ###
recruiter_data = test_data[8]["recruiter"]
company_id = recruiter_data["company_id"]
first_name = recruiter_data["first_name"]
last_name = recruiter_data["last_name"]
title = recruiter_data["title"]
email = recruiter_data["email"]
linkedin = recruiter_data["linkedin"]

test_recruiter = crud.create_recruiter(company_id, first_name, last_name, title, email, linkedin)
model.db.session.add(test_recruiter)
model.db.session.commit()

### Create Employee test data ###
employee_data = test_data[9]["employee"]
company_id = employee_data["company_id"]
first_name = employee_data["first_name"]
last_name = employee_data["last_name"]
title = employee_data["title"]
email = employee_data["email"]
linkedin = employee_data["linkedin"]

test_employee = crud.create_employee(company_id, first_name, last_name, title, email, linkedin)
model.db.session.add(test_employee)
model.db.session.commit()

### Don't need to create task_employee_index data. Can create during testing/building ###


print("🚨 Database has been seeded 🚨")