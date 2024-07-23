from flask import Flask
from flask_migrate import Migrate
import os
import model

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')

# Connect to the database
model.connect_to_db(app)

# Initialize Flask-Migrate
migrate = Migrate(app, model.db)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv('PORT', 5432)), debug=False)
