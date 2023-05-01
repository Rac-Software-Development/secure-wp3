from flask import Flask
from flask import render_template, flash, redirect, url_for, session
from datetime import datetime

# from config import Config

from flask_sqlalchemy import SQLAlchemy
import os
import sys

import sqlite3
from flask import request
from flask import jsonify
from datetime import datetime

app = Flask(__name__)
app.app_context().push()
SECRET_KEY = os.urandom(32)
db = SQLAlchemy()
app.config["SECRET_KEY"] = "Nh25"
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:////Users/Nizar/OneDrive - Hogeschool Rotterdam/Bureaublad/wp3 inhaalsopdracht/werkplaats-3---inhaalopdracht-Nizar-1012373"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.route("/")
@app.route("/Dashboard")
def Dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)
