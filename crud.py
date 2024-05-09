""" CRUD file for all CRUD functions"""

import model, hashlib
from pdb import set_trace
from datetime import datetime


def create_user(first_name, last_name, email, password, location, school, bio, headshot):

    ### Hash password here with haslib ###

    new_user = model.Users(
        first_name = first_name, 
        last_name = last_name,
        email = email,
        password = password, 
        location = location, 
        school = school, 
        bio = bio, 
        headshot = headshot
        )
    
    return new_user

########## Company Object ###########


def create_company(name, location, industry, favorite):
    new_company = model.Company(
        name = name, 
        location = location, 
        industry = industry, 
        favorite = favorite
        )
    return new_company

def show_all_companies_by_userID(user_id):
    company_list = model.Company.query.all()
    filtered_list = []
    for company in company_list:                        ### 🚨 this can be optimized ###
        if company.job[0].user_id == user_id:           ###  💡 filtering out companies that don't belong to user
            filtered_list.append(company)
    return filtered_list

def get_company_by_job_id(job_id):
    job = model.Job.query.get(job_id)
    company = job.company
    return company

########### Job Object ##########

def create_job(company_id, user_id, recruiter_id, role, description, requirements, salary, compensation, link, date_applied, job_offer, rejection, interviewing, accepted_offer, ghosted, favorite, last_logged_task, last_logged_task_time):
    new_job = model.Job(
        company_id = company_id, 
        user_id = user_id, 
        recruiter_id = recruiter_id, 
        role = role,
        description = description,
        requirements = requirements,
        salary = salary,
        compensation = compensation,
        link = link,
        date_applied = date_applied,
        job_offer = job_offer,
        rejection = rejection,
        interviewing = interviewing,
        accepted_offer = accepted_offer,
        ghosted = ghosted,
        favorite = favorite,
        last_logged_task = last_logged_task,
        last_logged_task_time = last_logged_task_time 
        )
    
    return new_job

def show_all_jobs_by_userID(user_id):
    job_list = model.Job.query.filter_by(user_id = user_id).all()           ### 💡filter all jobs by user_id
    return job_list

def job_detail(id):
    return model.Job.query.get(id)

def update_applied_status(job_id):
    job = model.Job.query.get(job_id)
    job.date_applied = datetime.now()
    return job

def update_bool(bool):
    if bool == False:
        bool = True
    else:
        bool = False
    return bool

def update_last_activity(job_id):
    job = model.Job.query.get("job_id")
    job.last_logged_task_time = datetime.now()
    return job

############# Email Object ########

def create_email(job_id, task_for_employee, task_for_recruiter, due_date, description, completed):
    new_email = model.Email(
        job_id = job_id,
        task_for_employee = task_for_employee,
        task_for_recruiter = task_for_recruiter,
        due_date = due_date,
        description = description,
        completed = completed
    )
    return new_email

def email_list_by_job(job_id):
    return model.Email.query.filter_by(job_id = job_id).all()

def get_email_by_id(call_id):
    return model.Email.query.get(call_id)

############ Call Object #########

def create_call(job_id, task_for_employee, task_for_recruiter, due_date, description, completed):
    new_call = model.Call(
        job_id = job_id,
        task_for_employee = task_for_employee,
        task_for_recruiter = task_for_recruiter,
        due_date = due_date,
        description = description,
        completed = completed
    )
    return new_call

def call_list_by_job(job_id):
    return model.Call.query.filter_by(job_id = job_id)

def get_call_by_id(call_id):
    return model.Call.query.get(call_id)
    

############# General Task Object ########

def create_general_task(job_id, task_for_employee, task_for_recruiter, due_date, description, completed):
    new_general_task = model.General_Task(
        job_id = job_id,
        task_for_employee = task_for_employee,
        task_for_recruiter = task_for_recruiter,
        due_date = due_date,
        description = description,
        completed = completed
    )
    return new_general_task

def general_task_by_job(job_id):
    return model.General_Task.query.filter_by(job_id = job_id)

def get_general_task_by_id(task_id):
    return model.General_Task.query.get(task_id)

############## Next Step Object #######

def create_next_step(job_id, task_for_employee, task_for_recruiter, due_date, description, step_type):
    new_next_step = model.Next_Step(
        job_id = job_id,
        task_for_employee = task_for_employee,
        task_for_recruiter = task_for_recruiter,
        due_date = due_date,
        description = description,
        step_type = step_type
    )
    return new_next_step

def next_step_list_by_job(job_id):
    return  model.Next_Step.query.filter_by(job_id = job_id)
    
############## Employee Object #######

def create_employee(company_id, first_name, last_name, title, email, linkedin):    
    new_employee = model.Employee(
        company_id = company_id,
        first_name = first_name,
        last_name = last_name,
        title = title,
        email = email,
        linkedin = linkedin
    )
    return new_employee

def employee_list_by_company(company_id):
    return model.Employee.query.filter_by(company_id = company_id)

def employee_list_by_job(job_id):
    return model.Employee.query.filter_by(job_id = job_id)
    
############# Recruiter Object ########

def create_recruiter(company_id, first_name, last_name, title, email, linkedin):
    new_recruiter = model.Recruiter(
        company_id = company_id,
        first_name = first_name,
        last_name = last_name,
        title = title,
        email = email,
        linkedin = linkedin
    )
    return new_recruiter

def recruiter_list_by_company(company_id):
    return model.Recruiter.query.filter_by(company_id = company_id)

def recruiter_list_by_job(job_id):
    return model.Recruiter.query.filter_by(job_id = job_id)



############## Miscellaneous Functions #######

def days_since(date_time):
    time_difference = datetime.now() - date_time
    return time_difference.days




