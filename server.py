""" server to contain endpoints for Wabbit app """

from flask import Flask, render_template



app = Flask(__name__)



@app.route("/")
def homepage():
    return render_template("homepage.html")










if __name__ == "__main__":

    app.run(host="localhost", port=4040, debug=True )