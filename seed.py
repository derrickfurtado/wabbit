""" Seed file to create/delete DB and add test data to our Wabbit DB for testing/building only"""

import os, model, server
from pdb import set_trace           

server.app.app_context().push()

os.system("dropdb wabbit")              ## drop table and all data
os.system("createdb wabbit")            ## recreate table

model.connect_to_db(server.app)         ## connect to Wabbit DB
model.db.create_all()                   ## create all tables



### 🚨 No longer need test data ###





# with open ('data/test_data.json') as file:  ## open and read .json file
#     test_data = json.loads(file.read())     ## test_data will be a list of dictionaries for each dataclass object



# ### Create Company test data ###
# company_data = test_data[2]["company"]
# name = company_data["name"]
# location = company_data["location"]
# industry = company_data["industry"]
# favorite = eval(company_data["favorite"])

# test_company = crud.create_company(name, location, industry, favorite)
# model.db.session.add(test_company)
# model.db.session.commit()


# ### Create User Test Data ###
# user_data = test_data[0]["users"]           ## each dataclass object has a specific index
# first_name = user_data["first_name"]
# last_name = user_data["last_name"]
# email = user_data["email"]
# password = key.user_password
# location = user_data["location"]
# school = user_data["school"]
# bio = user_data["bio"]
# headshot = user_data["headshot"]
# test_user = crud.create_user(first_name, last_name, email, password, location, school, bio, headshot)

# model.db.session.add(test_user)
# model.db.session.commit()


# ### Create Job Test Data ###
# job_data = test_data[1]["job"]
# company_id = job_data["company_id"]
# user_id = job_data["user_id"]
# role = job_data["role"]
# description = job_data["description"]
# requirements = job_data["requirements"]
# salary = job_data["salary"]
# compensation = job_data["compensation"]
# link = job_data["link"]
# date_applied = job_data["date_applied"]
# job_offer = eval(job_data["job_offer"])
# rejection = eval(job_data["rejection"])
# interviewing = eval(job_data["interviewing"])
# accepted_offer = eval(job_data["accepted_offer"])
# ghosted = eval(job_data["ghosted"])
# favorite = eval(job_data["favorite"])
# last_logged_task = job_data["last_logged_task"]
# last_logged_task_time = job_data["last_logged_task_time"]

# test_job = crud.create_job(company_id, user_id, None, role, description, requirements, salary, compensation, link, date_applied, job_offer, rejection, interviewing, accepted_offer, ghosted, favorite, last_logged_task, last_logged_task_time)            ### added None to certain fields that required dependencies. Only needed upon creation of test data

# model.db.session.add(test_job)
# model.db.session.commit()


# ### Create Recruiter test data ###
# recruiter_data = test_data[3]["recruiter"]
# company_id = recruiter_data["company_id"]
# first_name = recruiter_data["first_name"]
# last_name = recruiter_data["last_name"]
# title = recruiter_data["title"]
# email = recruiter_data["email"]
# linkedin = recruiter_data["linkedin"]

# test_recruiter = crud.create_recruiter(company_id, first_name, last_name, title, email, linkedin)
# model.db.session.add(test_recruiter)
# model.db.session.commit()

# ### Create Employee test data ###
# employee_data = test_data[4]["employee"]
# company_id = employee_data["company_id"]
# first_name = employee_data["first_name"]
# last_name = employee_data["last_name"]
# title = employee_data["title"]
# email = employee_data["email"]
# linkedin = employee_data["linkedin"]

# test_employee = crud.create_employee(company_id, first_name, last_name, title, email, linkedin)
# model.db.session.add(test_employee)
# model.db.session.commit()

# ### Don't need to create task_employee_index data. Can create during testing/building ###


print("🚨 Database has been seeded 🚨")