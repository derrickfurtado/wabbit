""" server to contain endpoints for Wabbit app """

import forms, model, crud
from flask import Flask, render_template, flash, redirect, session
from key import secret_key
from pdb import set_trace



app = Flask(__name__)
    

app.secret_key = secret_key                 ## secret key stored in key.py file for security


@app.route("/")                             ## main landing page
def login():
    login_form = forms.User_Login_Form()
    register_form = forms.User_Registration_Form()
    return render_template("login.html", login_form = login_form, register_form = register_form)

@app.route("/homepage")                     ## landing page, post login
def homepage():
    return render_template("homepage.html")

@app.route("/job_page")                       ## landing page for job creation
def show_job_form():
    job_form = forms.Job_Form()
    return render_template("/job_page.html", job_form = job_form)

@app.route("/create_company")                   ## landing page for company creation
def create_company():
    return render_template("/create_company.html")

############################################

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

@app.route("/create_job")
def create_job():
    
    redirect("/job_page")




if __name__ == "__main__":
    model.connect_to_db(app)
    app.run(host="localhost", port=4040, debug=True)