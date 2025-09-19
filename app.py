from flask import Flask
from flask import render_template
from flask import request
from os import getenv
import mysql.connector


mysql_user = getenv("MYSQL_USER")
mysql_pass = getenv("MYSQL_PASS")
mysql_host = getenv("MYSQL_HOST")
mysql_database = getenv("MYSQL_DATABASE")
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        print(request.form["task"])
    return render_template("index.html")
