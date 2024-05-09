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

def create_email(job_id, task_for_id, due_date, description, completed):
    new_email = model.Email(
        job_id = job_id,
        task_for_id = task_for_id,
        due_date = due_date,
        description = description,
        completed = completed
    )
    return new_email

############ Call Object #########

def create_call(job_id, task_for_id, due_date, description, completed):
    new_call = model.Call(
        job_id = job_id,
        task_for_id = task_for_id,
        due_date = due_date,
        description = description,
        completed = completed
    )
    return new_call

############# General Task Object ########

def create_general_task(job_id, task_for_id, due_date, description, completed):
    new_general_task = model.General_Task(
        job_id = job_id,
        task_for_id = task_for_id,
        due_date = due_date,
        description = description,
        completed = completed
    )
    return new_general_task

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
    employee_list = model.Employee.query.filter_by(company_id = company_id)
    return employee_list

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
    recruiter_list = model.Recruiter.query.filter_by(company_id = company_id)
    return recruiter_list

############## Miscellaneous Functions #######

def days_since(date_time):
    time_difference = datetime.now() - date_time
    return time_difference.days




