""" server to contain endpoints for Wabbit app """

import forms, model, crud
from flask import Flask, render_template, flash, redirect, session, request, url_for
from key import secret_key
from pdb import set_trace
from datetime import datetime



app = Flask(__name__)
    

app.secret_key = secret_key                 ## secret key stored in key.py file for security

############################ Credentials ##############################

@app.route("/")                             ## main landing page
def login_page():
    login_form = forms.User_Login_Form()
    register_form = forms.User_Registration_Form()
    return render_template("login.html", login_form = login_form, register_form = register_form)

@app.route("/login_user", methods=["POST"])                               ## check for errors if methods = ["POST"] is needed
def login_user():
    user_form = forms.User_Login_Form()             ## pull form data from login form
    current_users = model.Users.query.all()         ## query list of current users
    user_list = []                                  ## empty list for verified emails

    if user_form.validate_on_submit():
            user_found = False
            for user in current_users:
                if user_form.email.data == user.email:
                    user_found = True
                    if user_form.password.data == user.password:
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
        user_list.append(user.email)
    if register_form.validate_on_submit():
        if register_form.email.data not in user_list:
            first_name = register_form.first_name.data
            last_name = register_form.last_name.data
            email = register_form.email.data
            password = register_form.password.data

            new_user = crud.create_user(first_name, last_name, email, password, None, None, None, None)
            model.db.session.add(new_user)
            model.db.session.commit()
            flash("Successfully Registered Account")
            return redirect("/")
        else:
            flash("Email already exists")
            return redirect("/")
    else:
        flash("Error submitting form. Please Try again")
        return redirect("/")

@app.route("/sign_out")
def sign_out():
    del session["user_id"]
    flash(f"You have logged out!")
    return redirect("/")

############################ Homepage Routes ##############################

@app.route("/homepage")                     ## landing page, post login
def homepage():
    job_list = crud.show_all_jobs()
    company_list = crud.show_all_companies()

    return render_template("homepage.html", job_list = job_list, company_list = company_list)

            ####### 🚨 Add in table columns for buttons that update task completed

########################### Job Object ###############################


@app.route("/job_page")                        ### landing page for job creation form ###
def show_job_form():
    company_list = crud.show_all_companies()
    job_form = forms.Job_Form()
    choices = [(company.id, company.name) for company in company_list]      ## creating dynamic list for company options
    choices.append(("create_company", "*** Create Company ***"))            ## adding fall back in case company is not created yet
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
        declined_offer = False
        accepted_offer = False
        ghosted = False
        favorite = False
        last_logged_task = "Created Job"
        last_logged_task_time = datetime.now()
            ########################################## 🚨 implement auto tasks here

        new_job = crud.create_job(company_id, user_id, recruiter_id, role, description, requirements, salary, compensation, link, date_applied, job_offer, rejection, declined_offer, accepted_offer, ghosted, favorite, last_logged_task, last_logged_task_time)

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
    updated_job = crud.update_applied_status(job_id)
    model.db.session.add(updated_job)
    model.db.session.commit()

    return redirect(url_for('show_job_detail', job_id = job_id))

@app.route("/update_offer")
def update_offer():
    job_id = request.args.get("job_id")                 ### grab job_id from url parameter
    job = crud.job_detail(job_id)                       ### grab the job object using using job_id
    job.job_offer = crud.update_bool(job.job_offer)     ### switch values of boolean
    
    model.db.session.add(job)
    model.db.session.commit()
    
    return redirect(url_for('show_job_detail', job_id = job_id))

@app.route("/update_rejection")
def update_rejection():
    job_id = request.args.get("job_id")                 
    job = crud.job_detail(job_id)    
    job.rejection = crud.update_bool(job.rejection)

    model.db.session.add(job)
    model.db.session.commit()

    return redirect(url_for('show_job_detail', job_id = job_id))

@app.route("/update_declined")
def update_declined():
    job_id = request.args.get("job_id")                 
    job = crud.job_detail(job_id)    
    job.declined_offer = crud.update_bool(job.declined_offer)

    model.db.session.add(job)
    model.db.session.commit()

    return redirect(url_for('show_job_detail', job_id = job_id))

@app.route("/update_accepted")
def update_accepted():
    job_id = request.args.get("job_id")                 
    job = crud.job_detail(job_id)    
    job.accepted_offer = crud.update_bool(job.accepted_offer)

    model.db.session.add(job)
    model.db.session.commit()

    return redirect(url_for('show_job_detail', job_id = job_id))

@app.route("/update_ghosted")
def update_ghosted():
    job_id = request.args.get("job_id")                 
    job = crud.job_detail(job_id)    
    job.ghosted = crud.update_bool(job.ghosted)

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
    declined_offer = False
    accepted_offer = False
    ghosted = False
    favorite = False
    last_logged_task = "Created Job"
    last_logged_task_time = datetime.now()
        ########################################## 🚨 implement auto tasks here

    new_job = crud.create_job(company_id, user_id, recruiter_id, role, description, requirements, salary, compensation, link, date_applied, job_offer, rejection, declined_offer, accepted_offer, ghosted, favorite, last_logged_task, last_logged_task_time)

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

@app.route("/company_detail")
def show_company_detail():
    return render_template("company_detail_page.html")

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





@app.route("/sne_recruiter_form")
def sne_recruiter_form():
    sne_form = forms.SNE_Recruiter_Form()
    job_id = request.args.get("job_id")
    recruiter_list = crud.recruiter_list_by_company(job_id)
    choices = [(recruiter.id, f"{recruiter.first_name} {recruiter.last_name} ({recruiter.title})") for recruiter in recruiter_list]
    choices.append(("create_recruiter", "** Create Recruiter **"))
    sne_form.task_for_recruiter_id.choices = choices

    return render_template("sne_recruiter_form.html", sne_form = sne_form, job_id = job_id)

@app.route("/create_sne_4recruiter", methods=["post"])
def create_sne_4recruiter():
    job_id = request.args.get("job_id")
    sne_form = forms.SNE_Recruiter_Form()

    if sne_form.task_for_recruiter_id.data == "create_recruiter":
        ### forward form data to /sne_create_recruiter
        session["due_date"] = sne_form.due_date.data
        session["description"] = sne_form.description.data
        session["step_type"] = sne_form.step_type.data
        recruiter_form = forms.Recruiter_Form()

        return render_template("/create_recruiter_4sne.html", job_id = job_id, recruiter_form = recruiter_form)
    else:
        task_for_employee = None
        task_for_recruiter = sne_form.task_for_recruiter_id.data
        due_date = sne_form.due_date.data
        description = sne_form.description.data
        step_type = sne_form.step_type.data

        new_sne = crud.create_next_step(job_id, task_for_employee, task_for_recruiter, due_date, description, step_type)
        model.db.session.add(new_sne)
        model.db.session.commit()

        return redirect(url_for('show_job_detail', job_id = job_id))

@app.route("/create_recruiter_4sne_form")
def create_recruiter_4sne_form():
    job_id = request.args.get("job_id")
    recruiter_form = forms.Recruiter_Form()

    return render_template("create_recruiter_4sne.html", job_id = job_id, recruiter_form = recruiter_form)

@app.route("/add_recruiter_sne", methods=["post"])
def add_recruiter_sne():
    job_id = request.args.get("job_id")
    form = forms.Recruiter_Form()
    company = crud.get_company_by_job_id(job_id)
    company_id = company.id
    first_name = form.first_name.data
    last_name = form.last_name.data
    title = form.title.data
    email = form.email.data
    linkedin = form.linkedin.data
    new_recruiter = crud.create_recruiter(company_id, first_name, last_name, title, email, linkedin)
    model.db.session.add(new_recruiter)
    model.db.session.commit()

    task_for_employee = None
    task_for_recruiter = new_recruiter.id
    due_date = session["due_date"]
    del session["due_date"]
    description = session["description"]
    del session["description"]
    step_type = session["step_type"]
    del session["step_type"]

    new_sne = crud.create_next_step(job_id, task_for_employee, task_for_recruiter, due_date, description, step_type)
    model.db.session.add(new_sne)
    model.db.session.commit()

    return redirect(url_for("show_job_detail", job_id = job_id))


@app.route("/sne_employee_form")
def sne_employee_form():
    pass

@app.route("/create_sne_4employee", methods=["post"])
def create_sne_4employee():
    pass

@app.route("/create_employee_4sne_form")
def create_employee_4sne_form():
    pass

@app.route("/add_employee_sne", methods=["post"])
def add_employee_sne():
    pass







if __name__ == "__main__":
    model.connect_to_db(app)
    app.run(host="localhost", port=4040, debug=True)