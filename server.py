""" server to contain endpoints for Wabbit app """

from flask import Flask, render_template
from key import secret_key



app = Flask(__name__)


app.secret_key = secret_key


@app.route("/")
def login():
    return render_template("login.html")

@app.route("/homepage")
def homepage():
    return render_template("homepage.html")

@app.route("/register")
def create_account():
    return render_template("/register.html")

@app.route("/create_job")
def create_job():
    return render_template("/create_job.html")

@app.route("/create_company")
def create_company():
    return render_template("/create_company.html")


if __name__ == "__main__":

    app.run(host="localhost", port=4040, debug=True)