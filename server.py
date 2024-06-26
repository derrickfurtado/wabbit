""" server to contain endpoints for Wabbit app """

import forms, model, crud, bcrypt
from flask import Flask, render_template, flash, redirect, session, request, url_for
from key import secret_key
from pdb import set_trace
from datetime import datetime
import os



app = Flask(__name__)
    

app.secret_key = secret_key                 ### 💡secret key stored in key.py file for security

############################ Credentials ##############################

@app.route("/")                             ## main landing page
def login_page():
    login_form = forms.User_Login_Form()
    register_form = forms.User_Registration_Form()
    return render_template("login.html", login_form = login_form, register_form = register_form)

@app.route("/login_user", methods=["POST"])                               
def login_user():
    user_form = forms.User_Login_Form()             ## pull form data from login form
    current_users = model.Users.query.all()         ## query list of current users


    if user_form.validate_on_submit():
            user_found = False
            for user in current_users:
                if user_form.email.data == user.email:
                    user_found = True
                    user_password = user_form.password.data
                    user_byt_pass = user_password.encode('utf-8')
                    stored_password = user.password
                    password_check = bcrypt.checkpw(user_byt_pass, stored_password)
                    if password_check:
                        session["user_id"] = user.id
                        flash(f"Welcome back {user.first_name}!")
                        return redirect("/homepage")
                    else:
                        flash("Incorrect password. Try again.")
                        return redirect("/")
            if not user_found:
                flash("Account does not exist. Please register below.")
                return redirect("/")
    else:
        flash("Error submitting form. Please Try again")
        return redirect("/")

@app.route("/register_user", methods=["POST"])
def register_user():
    register_form = forms.User_Registration_Form()  ## capture form data
    current_users = model.Users.query.all()         ## query list of current users
    user_list = []                                  ## empty list for verified emails

    for user in current_users:
        user_list.append(user.email)              ### 💡 doing this so only email is being stored in a list, not passwords     
    if register_form.validate_on_submit():
        if register_form.email.data not in user_list:
            first_name = register_form.first_name.data
            last_name = register_form.last_name.data
            email = register_form.email.data
            password = register_form.password.data                  ### 🚨 bcrypt here

            
            byt = password.encode('utf-8')
            salt = bcrypt.gensalt()

            password = bcrypt.hashpw(byt, salt)


            new_user = crud.create_user(first_name, last_name, email, password, None, None, None, None)
            model.db.session.add(new_user)
            model.db.session.commit()
            flash("Successfully Registered Account")
            return redirect("/")
        else:
            flash("Email already exists. Choose a different email.")
            return redirect("/")
    else:
        flash("Error submitting form. Please Try again")
        return redirect("/")

@app.route("/sign_out")
def sign_out():
    del session["user_id"]
    return redirect("/")

############################ Homepage Routes ##############################

@app.route("/homepage")                     ## landing page, post login
def homepage():
    user_id = session["user_id"]
    job_list = crud.show_all_jobs_by_userID(user_id)               ### 💡only pull jobs that the user owns in the DB
    

    if not job_list:
        flash("You are not tracking any opportunities. Get on it!!!")
    return render_template("homepage.html", job_list = job_list, user_id = user_id)

            ####### 🚨 Add in table columns for buttons that update task completed

@app.route("/company_list")
def company_list():
    company_list = crud.show_all_companies_by_userID(session["user_id"])
    return render_template("companies.html", company_list = company_list)


@app.route("/archived_jobs")
def archived_jobs():
    job_list = crud.show_all_jobs_by_userID(session["user_id"])
    return render_template("archived_jobs.html", job_list = job_list)


########################### Job Object ###############################


@app.route("/job_page")                        ### landing page for job creation form ###
def show_job_form():
    company_list = crud.show_all_companies_by_userID(session["user_id"])
    job_form = forms.Job_Form()
    choices = [(company.id, company.name) for company in company_list]      ## creating dynamic list for company options
    choices.insert(0,("create_company", "*** Create Company ***"))            ## adding fall back in case company is not created yet
    job_form.company.choices = choices                              ## adding dynamic list and fallback together to choices

    return render_template("/job_page.html", job_form = job_form)

@app.route("/create_job", methods=["POST"])
def create_job():
    job_form = forms.Job_Form()

                                                        ####### can I put validate on submit here?
    if job_form.company.data == 'create_company':
        session["role"] = job_form.role.data
        session["description"] = job_form.description.data
        session["requirements"] = job_form.requirements.data
        session["salary"] = job_form.salary.data
        session["compensation"] = job_form.compensation.data
        session["link"] = job_form.link.data

        return redirect("company_page")
    
    else:
        company_id = job_form.company.data
        user_id = session["user_id"]
        recruiter_id = None
        role = job_form.role.data
        description = job_form.description.data
        requirements = job_form.requirements.data
        salary = job_form.salary.data
        compensation = job_form.compensation.data
        link = job_form.link.data
        date_applied = None
        job_offer = False
        rejection = False
        interviewing = False
        accepted_offer = False
        ghosted = False
        favorite = False
        last_logged_task = "Created Job"
        last_logged_task_time = datetime.now()
            ########################################## 🚨 implement auto tasks here

        new_job = crud.create_job(company_id, user_id, recruiter_id, role, description, requirements, salary, compensation, link, date_applied, job_offer, rejection, interviewing, accepted_offer, ghosted, favorite, last_logged_task, last_logged_task_time)

        model.db.session.add(new_job)
        model.db.session.commit()
        flash(f"Job Created! Let's keep going!")
        return redirect("/job_page")

@app.route("/job_detail")
def show_job_detail():
    job_id = request.args.get('job_id')
    job = crud.job_detail(job_id)
    days_since_task = crud.days_since(job.last_logged_task_time)
    return render_template("job_detail_page.html", job = job, days_since_task = days_since_task)

@app.route("/update_applied_status")
def update_applied_status():
    job_id = request.args.get("job_id")
    updated_job = crud.update_applied_status(job_id)        ### 💡 updated applied status to job 
    updated_job.last_logged_task = "Submitted Application"  ### 💡 updated last task
    updated_job.last_logged_task_time = datetime.now()      ### 💡 updated last task time to now
    model.db.session.add(updated_job)
    model.db.session.commit()

    return redirect(url_for('show_job_detail', job_id = job_id))

@app.route("/remove_applied_date")
def remove_applied_date():

    job_id = request.args.get("job_id")
    updated_job = crud.remove_applied_status(job_id)
    updated_job.last_logged_task = "Created Job"
    model.db.session.add(updated_job)
    model.db.session.commit()
    return redirect(url_for("show_job_detail", job_id = job_id))

@app.route("/update_offer")
def update_offer():
    job_id = request.args.get("job_id")                 ### grab job_id from url parameter
    job = crud.job_detail(job_id)                       ### grab the job object using using job_id
    job.job_offer = crud.update_bool(job.job_offer)     ### switch values of boolean
    job.last_logged_task = "Received Job Offer"
    job.last_logged_task_time = datetime.now()


    model.db.session.add(job)
    model.db.session.commit()
    
    return redirect(url_for('show_job_detail', job_id = job_id))

@app.route("/update_rejection")
def update_rejection():
    job_id = request.args.get("job_id")                 
    job = crud.job_detail(job_id)    
    job.rejection = crud.update_bool(job.rejection)
    job.last_logged_task = "Received Rejection Notice"
    job.last_logged_task_time = datetime.now()

    model.db.session.add(job)
    model.db.session.commit()

    return redirect(url_for('show_job_detail', job_id = job_id))

@app.route("/update_interviewing")
def update_interviewing():
    job_id = request.args.get("job_id")                 
    job = crud.job_detail(job_id)    
    job.interviewing = crud.update_bool(job.interviewing)
    job.last_logged_task = "Starting Interview Process"
    job.last_logged_task_time = datetime.now()

    model.db.session.add(job)
    model.db.session.commit()

    return redirect(url_for('show_job_detail', job_id = job_id))

@app.route("/update_accepted")
def update_accepted():
    job_id = request.args.get("job_id")                 
    job = crud.job_detail(job_id)    
    job.accepted_offer = crud.update_bool(job.accepted_offer)
    job.last_logged_task = "Accepted Offer"
    job.last_logged_task_time = datetime.now()

    model.db.session.add(job)
    model.db.session.commit()

    return redirect(url_for('show_job_detail', job_id = job_id))

@app.route("/update_ghosted")
def update_ghosted():
    job_id = request.args.get("job_id")                 
    job = crud.job_detail(job_id)    
    job.ghosted = crud.update_bool(job.ghosted)
    job.last_logged_task = "You've been Ghosted"
    job.last_logged_task_time = datetime.now()

    model.db.session.add(job)
    model.db.session.commit()

    return redirect(url_for('show_job_detail', job_id = job_id))

@app.route("/update_favorite")
def update_favorite():
    job_id = request.args.get("job_id")                 
    job = crud.job_detail(job_id)    
    job.favorite = crud.update_bool(job.favorite)

    model.db.session.add(job)
    model.db.session.commit()

    return redirect(url_for('show_job_detail', job_id = job_id))

@app.route("/update_favorite_homepage")
def update_favorite_homepage():
    job_id = request.args.get("job_id")                 
    job = crud.job_detail(job_id)    
    job.favorite = crud.update_bool(job.favorite)

    model.db.session.add(job)
    model.db.session.commit()

    return redirect(url_for('homepage'))

@app.route("/next_steps")
def schedule_next_step():
    next_step_form = forms.Next_Step_Form()

    job_id = request.args.get("job_id")
    job = crud.job_detail(job_id)

    recruiter_list = crud.recruiter_list_by_company(job.company_id)
    employee_list = crud.employee_list_by_company(job.company_id)
    
    recruiter_choices = [(recruiter.id, f"{recruiter.first_name} {recruiter.last_name} ({recruiter.title})") for recruiter in recruiter_list]
    employee_choices = [(employee.id, f"{employee.first_name} {employee.last_name} ({employee.title})" ) for employee in employee_list]

    recruiter_choices.append(("add_recruiter", "*** Create Recruiter ***"))
    recruiter_choices.append(("no_recruiter", "Not meeting with Recruiter"))
    employee_choices.append(("add employee", "*** Create Employee ***"))
    employee_choices.append(("no_employee", "Not meeting with Employee"))

    next_step_form.task_for_recruiter_id.choices = recruiter_choices
    next_step_form.task_for_employee_id.choices = employee_choices

    return render_template("next_step_form.html", next_step_form = next_step_form, job_id = job_id)

@app.route("/create_next_step", methods=["post"])
def create_next_step():
    next_step_form = forms.Next_Step_Form()
    job_id = request.args.get("job_id")
    
    task_for_recruiter = next_step_form.task_for_recruiter_id.data
    task_for_employee = next_step_form.task_for_employee_id.data
    due_date = next_step_form.due_date.data
    description = next_step_form.description.data
    step_type = next_step_form.step_type.data
    
    if task_for_employee != "no_employee" and task_for_recruiter != "no_recruiter":
        new_next_step = crud.create_next_step(job_id, task_for_employee, task_for_recruiter, due_date, description, step_type)
        model.db.session.add(new_next_step)
        model.db.session.commit()
    elif task_for_employee != "no_employee" and task_for_recruiter == "no_recruiter":
        task_for_recruiter = None
        new_next_step = crud.create_next_step(job_id, task_for_employee, task_for_recruiter, due_date, description, step_type)
        model.db.session.add(new_next_step)
        model.db.session.commit()
    elif task_for_employee == "no_employee" and task_for_recruiter != "no_recruiter":
        task_for_employee = None
        new_next_step = crud.create_next_step(job_id, task_for_employee, task_for_recruiter, due_date, description, step_type)
        model.db.session.add(new_next_step)
        model.db.session.commit()

    return redirect(url_for('show_job_detail', job_id = job_id))

@app.route("/delete_warning")
def delete_warning():
    job_id = request.args.get("job_id")
    gif = crud.loop_gifs()

    return render_template("delete_warning.html", job_id = job_id, gif = gif)

@app.route("/delete_job")
def delete_job():
    job_id = request.args.get("job_id")
    job = crud.get_job_by_id(job_id)

    next_step_list = crud.next_step_list_by_job(job_id)
    email_list = crud.email_list_by_job(job_id)
    call_list = crud.call_list_by_job(job_id)
    task_list = crud.general_task_by_job(job_id)

    for step in next_step_list:
        model.db.session.delete(step)
    for email in email_list:
        model.db.session.delete(email)
    for call in call_list:
        model.db.session.delete(call)
    for task in task_list:
        model.db.session.delete(task)

    model.db.session.delete(job)
    model.db.session.commit()

    flash("Job has been deleted.")
    return redirect("homepage")

########################### Company Object ###############################

@app.route("/company_page")                                                 ## landing page for company creation
def show_company_form():
    company_form = forms.Company_Form()
    return render_template("company_page.html", company_form = company_form)

@app.route("/create_company", methods=["post"])                             ## landing page for company creation AFTER job creation, IF company does not exist            
def create_company():
    company_form = forms.Company_Form()

    name = company_form.name.data
    location = company_form.location.data
    industry = company_form.industry.data
    favorite = False
    
    new_company = crud.create_company(name, location, industry, favorite)
    model.db.session.add(new_company)
    model.db.session.commit()               ### commit here to get the new_company.id index
    
    company_id = new_company.id             ### using new company id for this job created. Jobs require a company to be relational
    user_id = session["user_id"]                    
    recruiter_id = None
    role = session["role"]
    description = session["description"]                ##### pulling session data from job creation into this page
    requirements = session["requirements"]
    salary = session["salary"]
    compensation = session["compensation"]
    link = session["link"]
    date_applied = None
    job_offer = False
    rejection = False
    interviewing = False
    accepted_offer = False
    ghosted = False
    favorite = False
    last_logged_task = "Created Job"
    last_logged_task_time = datetime.now()
        ########################################## 🚨 implement auto tasks here

    new_job = crud.create_job(company_id, user_id, recruiter_id, role, description, requirements, salary, compensation, link, date_applied, job_offer, rejection, interviewing, accepted_offer, ghosted, favorite, last_logged_task, last_logged_task_time)

    del session["role"]                             ##### removing all of these unique sessions after they are no longer needed
    del session["description"]
    del session["requirements"]
    del session["salary"]
    del session["compensation"]
    del session["link"]

    model.db.session.add(new_job)
    model.db.session.commit()
    flash("Job and Company created! Keep it up!")
    return redirect("job_page")

@app.route("/show_company_detail")
def show_company_detail():
    company_id = request.args.get("company_id")
    company = crud.get_company_by_company_id(company_id)

    return render_template("company_detail.html", company = company)

@app.route("/update_favorite_company")
def update_favorite_company():
    company_id = request.args.get("company_id")
    company = crud.get_company_by_company_id(company_id)
    company.favorite = crud.update_bool(company.favorite)

    model.db.session.add(company)
    model.db.session.commit()

    return redirect(url_for("show_company_detail", company_id = company_id))

@app.route("/update_favorite_company_homepage")
def update_favorite_company_homepage():
    company_id = request.args.get("company_id")
    company = crud.get_company_by_company_id(company_id)
    company.favorite = crud.update_bool(company.favorite)
    company_list = crud.show_all_companies_by_userID(session["user_id"])

    model.db.session.add(company)
    model.db.session.commit()

    return redirect(url_for("company_list", company_list = company_list))

######################### People Objects #################################

@app.route("/create_recruiter_form")
def create_recruiter_form():
    job_id = request.args.get("job_id")
    recruiter_form = forms.Recruiter_Form()
    return render_template("create_recruiter.html", recruiter_form = recruiter_form, job_id = job_id)

@app.route("/create_recruiter", methods=["post"])
def create_recruiter():
    recruiter_form = forms.Recruiter_Form()
    job_id = request.args.get("job_id")
    job = model.Job.query.get(job_id)
    company_id = job.company_id
    first_name = recruiter_form.first_name.data
    last_name = recruiter_form.last_name.data
    title = recruiter_form.title.data
    email = recruiter_form.email.data
    linkedin = recruiter_form.linkedin.data
    
    new_recruiter = crud.create_recruiter(company_id, first_name, last_name, title, email, linkedin)        ### create recruiter
    model.db.session.add(new_recruiter)
    model.db.session.commit()
    
    job.recruiter_id = new_recruiter.id
    model.db.session.add(job)
    model.db.session.commit()

    flash("Recruiter added to Job")
    return render_template("job_detail_page.html", job = job)

@app.route("/create_employee_form")
def create_employee_form():
    company_id = request.args.get("company_id")
    job_id = request.args.get("job_id")
    employee_form = forms.Employee_Form()
    return render_template("create_employee.html", employee_form = employee_form, company_id = company_id, job_id = job_id)

@app.route("/create_employee", methods=["post"])
def create_employee():
    company_id = request.args.get("company_id")
    job_id = request.args.get("job_id")
    employee_form = forms.Employee_Form()
    first_name = employee_form.first_name.data
    last_name = employee_form.last_name.data
    title = employee_form.title.data
    email = employee_form.email.data
    linkedin = employee_form.linkedin.data

    new_employee = crud.create_employee(company_id, first_name, last_name, title, email, linkedin)
    model.db.session.add(new_employee)
    model.db.session.commit()

    flash(f"Stakeholder added to {new_employee.company.name}")
    return redirect(url_for("show_job_detail", job_id = job_id))



############## Next Step End Points ####################

@app.route("/sne_recruiter_form")
def sne_recruiter_form():
    sne_form = forms.SNE_Recruiter_Form()                   ### 💡 pull in form template
    job_id = request.args.get("job_id")                     ### 💡 this job_id is hitching a ride
    company = crud.get_company_by_job_id(job_id)                    ### 💡 need this to get all recruiters in company
    recruiter_list = crud.recruiter_list_by_company(company.id)

    categories = [("Phone Call", "Phone Call"), ("Zoom Call","Zoom Call"), ("Google Meet","Google Meet"), ("In Person","In Person")]
    sne_form.step_type.choices = categories

    choices = [(recruiter.id, f"{recruiter.first_name} {recruiter.last_name} ({recruiter.title})") for recruiter in recruiter_list]   ### 💡 creating a dynamic list for creating next steps
    choices.insert(0, ("create_recruiter", "*** Create Recruiter ***"))        ### 💡 adding option, in case recruiter object is absent
    sne_form.task_for_recruiter_id.choices = choices            ### 💡 assigning choices to this form before rendering

    return render_template("sne_recruiter_form.html", sne_form = sne_form, job_id = job_id)

@app.route("/create_sne_4recruiter", methods=["post"])
def create_sne_4recruiter():
    job_id = request.args.get("job_id")
    sne_form = forms.SNE_Recruiter_Form()
    if sne_form.task_for_recruiter_id.data == "create_recruiter":                   ### 💡 if "Create Recruiter" is selected on the form
        session["due_date"] = sne_form.due_date.data

        session["due_time"] = str(sne_form.due_time.data)                           ### 💡 Session cannot store datetime.time data so need to convert to string
        session["description"] = sne_form.description.data                          ### 💡 saving form data to session
        session["step_type"] = sne_form.step_type.data
        recruiter_form = forms.Recruiter_Form()

        return render_template("/create_recruiter_4sne_form.html", job_id = job_id, recruiter_form = recruiter_form)
    else:
        task_for_employee = None                                            ### 💡 this next step is for recruiter, not employee. DB column is nullable
        task_for_recruiter = sne_form.task_for_recruiter_id.data
        due_date = sne_form.due_date.data
        due_time = sne_form.due_time.data
        description = sne_form.description.data
        step_type = sne_form.step_type.data

        new_sne = crud.create_next_step(job_id, task_for_employee, task_for_recruiter, due_date, due_time, description, step_type)
        model.db.session.add(new_sne)                                       ### 💡 create next step object

        job = crud.get_job_by_id(job_id)
        job.recruiter_id = sne_form.task_for_recruiter_id.data              ### 💡 add this recruiter to the Lead Recruiter of the job
        job.interviewing = True
        model.db.session.add(job)
        model.db.session.commit()

        return redirect(url_for('show_job_detail', job_id = job_id))

@app.route("/create_recruiter_4sne_form")
def create_recruiter_4sne_form():
    job_id = request.args.get("job_id")
    recruiter_form = forms.Recruiter_Form()             ### 💡 reusing recruiter form

    return render_template("create_recruiter_4sne.html", job_id = job_id, recruiter_form = recruiter_form)

@app.route("/add_recruiter_sne", methods=["post"])
def add_recruiter_sne():
    job_id = request.args.get("job_id")                 ### 💡 job_id keeps hitching a ride to reuse when sending back to job detail page
    form = forms.Recruiter_Form()                       ### 💡 capture date from last form used
    company = crud.get_company_by_job_id(job_id)
    company_id = company.id
    first_name = form.first_name.data
    last_name = form.last_name.data
    title = form.title.data
    email = form.email.data
    linkedin = form.linkedin.data
    new_recruiter = crud.create_recruiter(company_id, first_name, last_name, title, email, linkedin)
    model.db.session.add(new_recruiter)
    model.db.session.commit()                           ### 💡 need to create recruiter first to get recruiter id for next step object

    task_for_employee = None
    task_for_recruiter = new_recruiter.id
    due_date = session["due_date"]                                                  ### 💡  pulling old form data from session dictionary
    
    time_object = datetime.strptime(session["due_time"], '%H:%M:%S')                   ### 💡 reverting back to datetime.time object
    due_time = time_object.time()
    
    description = session["description"]
    step_type = session["step_type"]
    
    del session["description"]                          ### 💡 making sure to delete session key/value pairs to not cause issues
    del session["due_date"] 
    del session["due_time"]
    del session["step_type"]

    new_sne = crud.create_next_step(job_id, task_for_employee, task_for_recruiter, due_date, due_time, description, step_type)
    model.db.session.add(new_sne)
    model.db.session.commit()

    job = crud.get_job_by_id(job_id)
    job.recruiter_id = new_recruiter.id            ### 💡 add this newly created recruiter to the Lead Recruiter of the job
    job.interviewing = True
    model.db.session.add(job)
    model.db.session.commit()

    return redirect(url_for("show_job_detail", job_id = job_id))

@app.route("/sne_employee_form")                    ### 💡 the following employee next step forms are same as recruiter
def sne_employee_form():
    sne_form = forms.SNE_Employee_Form()
    job_id = request.args.get("job_id")
    company = crud.get_company_by_job_id(job_id)
    employee_list = crud.employee_list_by_company(company.id)

    categories = [("Phone Call", "Phone Call"), ("Zoom Call","Zoom Call"), ("Google Meet","Google Meet"), ("In Person","In Person")]
    sne_form.step_type.choices = categories

    choices = [(employee.id, f"{employee.first_name} {employee.last_name} ({employee.title})") for employee in employee_list]
    choices.insert(0, ("create_employee", "*** Create Employee ***"))
    sne_form.task_for_employee_id.choices = choices

    return render_template("sne_employee_form.html", job_id = job_id, sne_form = sne_form)

@app.route("/create_sne_4employee", methods=["post"])
def create_sne_4employee():
    job_id = request.args.get("job_id")
    employee_form = forms.SNE_Employee_Form()

    if employee_form.task_for_employee_id.data == "create_employee":
        ### session and render template
        session["due_date"] = employee_form.due_date.data
        session["due_time"] = str(employee_form.due_time.data)
        session["description"] = employee_form.description.data
        session["step_type"] = employee_form.step_type.data

        return redirect(url_for('create_employee_4sne_form', job_id = job_id))
    else:
        task_for_employee = employee_form.task_for_employee_id.data
        task_for_recruiter = None
        due_date = employee_form.due_date.data
        due_time = employee_form.due_time.data
        description = employee_form.description.data
        step_type = employee_form.step_type.data
        new_task = crud.create_next_step(job_id, task_for_employee, task_for_recruiter, due_date, due_time, description, step_type)
        model.db.session.add(new_task)
        model.db.session.commit()

        job = crud.get_job_by_id(job_id)
        job.interviewing = True
        model.db.session.add(job)
        model.db.session.commit()

        return redirect(url_for("show_job_detail", job_id = job_id))

@app.route("/create_employee_4sne_form")
def create_employee_4sne_form():
    employee_form = forms.Employee_Form()
    job_id = request.args.get("job_id")

    return render_template("create_employee_4sne_form.html", job_id = job_id, employee_form = employee_form)

@app.route("/add_employee_sne", methods=["post"])
def add_employee_sne():
    job_id = request.args.get("job_id")
    company = crud.get_company_by_job_id(job_id)
    employee_form = forms.Employee_Form()

    company_id = company.id
    first_name = employee_form.first_name.data
    last_name = employee_form.last_name.data
    title = employee_form.title.data
    email = employee_form.email.data
    linkedin = employee_form.linkedin.data

    new_employee = crud.create_employee(company_id, first_name, last_name, title, email, linkedin)
    model.db.session.add(new_employee)
    model.db.session.commit()

    task_for_employee_id = new_employee.id
    task_for_recruiter_id = None
    due_date = session["due_date"]
    
    time_object = datetime.strptime(session["due_time"], '%H:%M:%S')
    due_time = time_object.time()

    description = session["description"]
    step_type = session["step_type"]
    
    del session["due_date"]
    del session["due_time"]
    del session["description"]
    del session["step_type"]

    new_task = crud.create_next_step(job_id, task_for_employee_id, task_for_recruiter_id, due_date, due_time, description, step_type)
    model.db.session.add(new_task)
    model.db.session.commit()

    job = crud.get_job_by_id(job_id)
    job.interviewing = True
    model.db.session.add(job)
    model.db.session.commit()

    return redirect(url_for("show_job_detail", job_id = job_id))

############################## Call End Points ################################

@app.route("/complete_call_task")
def complete_call_task():
    job_id = request.args.get("job_id")
    call_id = request.args.get("call_id")
    call = crud.get_call_by_id(int(call_id))
    call.completed = crud.update_bool(call.completed)
    call.job.last_logged_task_time = datetime.now()         
    call.job.last_logged_task = call.description

    model.db.session.add(call.job)
    model.db.session.add(call)
    model.db.session.commit()

    return redirect(url_for("show_job_detail", job_id = job_id))

@app.route("/call_form")
def call_form():
    job_id = request.args.get("job_id")
    form = forms.Call_Form()

    return render_template("call_form.html", form = form, job_id = job_id)

@app.route("/create_call_job", methods=["post"])
def create_call_job():
    form = forms.Call_Form()
    job_id = request.args.get("job_id")

    task_for_employee = None
    task_for_recruiter = None
    due_date = form.due_date.data
    description = form.description.data
    completed = False

    new_call = crud.create_call(job_id, task_for_employee, task_for_recruiter, due_date, description, completed)
    model.db.session.add(new_call)
    model.db.session.commit()

    return redirect(url_for('show_job_detail', job_id = job_id))

@app.route("/delete_call")
def delete_call():
    job_id = request.args.get("job_id")
    call_id = request.args.get("call_id")
    call = crud.get_call_by_id(call_id)

    model.db.session.delete(call)
    model.db.session.commit()

    flash("Call Task Deleted!")
    return redirect(url_for("show_job_detail", job_id = job_id))

############################## Email End Points ################################

@app.route("/complete_email_task")
def complete_email_task():
    job_id = request.args.get("job_id")
    email_id = request.args.get("email_id")
    email = crud.get_email_by_id(int(email_id))
    email.completed = crud.update_bool(email.completed)
    email.job.last_logged_task_time = datetime.now()
    email.job.last_logged_task = email.description

    model.db.session.add(email.job)
    model.db.session.add(email)
    model.db.session.commit()

    return redirect(url_for("show_job_detail", job_id = job_id))

@app.route("/email_form")
def email_form():
    job_id = request.args.get("job_id")
    form = forms.Email_Form()

    return render_template("email_form.html", form = form, job_id = job_id)

@app.route("/create_email_job", methods=["post"])
def create_email_job():
    form = forms.Email_Form()
    job_id = request.args.get("job_id")

    task_for_employee = None
    task_for_recruiter = None
    due_date = form.due_date.data
    description = form.description.data
    completed = False

    new_email = crud.create_email(job_id, task_for_employee, task_for_recruiter, due_date, description, completed)
    model.db.session.add(new_email)
    model.db.session.commit()

    return redirect(url_for('show_job_detail', job_id = job_id))

@app.route("/delete_email")
def delete_email():
    email_id = request.args.get("email_id")
    job_id = request.args.get("job_id")
    email = crud.get_email_by_id(email_id)

    model.db.session.delete(email)
    model.db.session.commit()

    flash("Email Task Deleted")
    return redirect(url_for('show_job_detail', job_id = job_id))

############################## General Task End Points ################################

@app.route("/complete_general_task")
def complete_general_task():
    job_id = request.args.get("job_id")
    task_id = request.args.get("task_id")
    task = crud.get_general_task_by_id(int(task_id))
    task.completed = crud.update_bool(task.completed)
    task.job.last_logged_task_time = datetime.now()
    task.job.last_logged_task = task.description

    model.db.session.add(task.job)
    model.db.session.add(task)
    model.db.session.commit()

    return redirect(url_for("show_job_detail", job_id = job_id))

@app.route("/task_form")
def task_form():
    job_id = request.args.get("job_id")
    form = forms.General_Task_Form()

    return render_template("task_form.html", form = form, job_id = job_id)

@app.route("/create_task_job", methods=["post"])
def create_task_job():
    form = forms.General_Task_Form()
    job_id = request.args.get("job_id")

    task_for_employee = None
    task_for_recruiter = None
    due_date = form.due_date.data
    description = form.description.data
    completed = False

    new_task = crud.create_general_task(job_id, task_for_employee, task_for_recruiter, due_date, description, completed)
    model.db.session.add(new_task)
    model.db.session.commit()

    return redirect(url_for('show_job_detail', job_id = job_id))

@app.route("/delete_general_task")
def delete_general_task():
    job_id = request.args.get("job_id")
    task_id = request.args.get("task_id")
    general_task = crud.get_general_task_by_id(task_id)

    model.db.session.delete(general_task)
    model.db.session.commit()

    flash("General Task Deleted!")
    return redirect(url_for('show_job_detail', job_id = job_id))









if __name__ == "__main__":
    model.connect_to_db(app)
    app.run(host="localhost", port=4040, debug=True)