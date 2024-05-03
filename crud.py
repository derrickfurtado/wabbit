""" CRUD file for all CRUD functions"""

import model, hashlib
from pdb import set_trace


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

#####################


def create_company(name, location, industry, favorite):
    new_company = model.Company(
        name = name, 
        location = location, 
        industry = industry, 
        favorite = favorite
        )
    
    return new_company

def show_all_companies():
    company_list = model.Company.query.all()
    return company_list

#####################

def create_job(company_id, user_id, recruiter_id, role, description, requirements, salary, compensation, link, date_applied, job_offer, rejection, declined_offer, accepted_offer, ghosted, favorite, last_logged_task, last_logged_task_time):
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
        declined_offer = declined_offer,
        accepted_offer = accepted_offer,
        ghosted = ghosted,
        favorite = favorite,
        last_logged_task = last_logged_task,
        last_logged_task_time = last_logged_task_time 
        )
    
    return new_job

#####################

def create_email(job_id, task_for_id, due_date, description, completed):
    new_email = model.Email(
        job_id = job_id,
        task_for_id = task_for_id,
        due_date = due_date,
        description = description,
        completed = completed
    )
    return new_email

#####################

def create_call(job_id, task_for_id, due_date, description, completed):
    new_call = model.Call(
        job_id = job_id,
        task_for_id = task_for_id,
        due_date = due_date,
        description = description,
        completed = completed
    )
    return new_call

#####################

def create_general_task(job_id, task_for_id, due_date, description, completed):
    new_general_task = model.General_Task(
        job_id = job_id,
        task_for_id = task_for_id,
        due_date = due_date,
        description = description,
        completed = completed
    )
    return new_general_task

#####################

def create_next_step(job_id, task_for_id, due_date, description, step_type):
    new_next_step = model.Next_Step(
        job_id = job_id,
        task_for_id = task_for_id,
        due_date = due_date,
        description = description,
        step_type = step_type
    )
    return new_next_step

#####################

def create_task_employee_index(employee_id, recruiter_id):
    new_index = model.Task_Employee_Index( 
        employee_id = employee_id,
        recruiter_id = recruiter_id
        )
    return new_index

#####################

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

#####################

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




