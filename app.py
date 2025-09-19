from flask import Flask
from flask import render_template
from flask import request
from os import getenv
import signal
import mysql.connector
from sys import exit


def shutdown(signum, frame):
    cursor.close()
    cnx.close()
    exit(0)


mysql_user = getenv("MYSQL_USER")
mysql_pass = getenv("MYSQL_PASS")
mysql_host = getenv("MYSQL_HOST")
cnx = mysql.connector.connect(user=mysql_user, password=mysql_pass, host=mysql_host)
cursor = cnx.cursor()
cursor.execute("SHOW DATABASES LIKE 'fun'")
if not cursor.fetchone():
    cursor.execute("CREATE DATABASE fun")
cursor.execute("USE fun")
cursor.execute("SHOW TABLES LIKE 'tasks'")
if not cursor.fetchone():
    cursor.execute("""
    CREATE TABLE tasks (
        task_id int NOT NULL AUTO_INCREMENT,
        task_content varchar(150),
        PRIMARY KEY (task_id)
    )
    """)
signal.signal(signal.SIGINT, shutdown)
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        cursor.execute(
            """
        INSERT INTO tasks (task_content)
        VALUES (%s)
        """,
            (request.form["task"],),
        )
        cnx.commit()
    return render_template("index.html")
