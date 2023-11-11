from flask import Flask, render_template, request, session, redirect
from werkzeug.utils import secure_filename
import sqlite3
import os
import uuid
import random

app = Flask(__name__)
app.secret_key = "~!@#$%^&*()_+QWERASDFGHJK"
DATA_BASE_FILE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'accounts_info2.sqlite')

def check_to_create_table():
    connection = sqlite3.connect(DATA_BASE_FILE_PATH)
    cur = connection.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS Accounts ( id INTEGER PRIMARY KEY, full_name TEXT NOT NULL, level TEXT NOT NULL, age TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL, previous_seven_subjects TEXT)')
    connection.commit()
    connection.close()
    
check_to_create_table()


@app.route('/account', methods=["POST", "GET"])
def account():    
    connection = sqlite3.connect(DATA_BASE_FILE_PATH)
    cur = connection.cursor()
    cur.execute("SELECT * FROM Accounts WHERE email=?", (session["logged_in_user"],))
    one_user = cur.fetchone()
        
    full_name = one_user[1]
    level = one_user[2]
    age = one_user[3]
    password = one_user[5]
        
    connection.close()
        
    return render_template("account.html", full_name=full_name, level=level, age=age, password=password)
    
@app.route('/account_update', methods=["POST"])
def account_update():
    new_full_name = request.values.get('full_name')
    new_level = request.form["proficiency"]
    new_age = request.values.get('age')
    new_password = request.values.get('password')
    email = session["logged_in_user"]
    
    connection = sqlite3.connect(DATA_BASE_FILE_PATH)
    cur = connection.cursor()
    cur.execute(
    "UPDATE Accounts SET full_name=?, level=?, age=?, password=? WHERE email=?",
    (new_full_name, new_level, new_age, new_password, email),)

    connection.commit()
    connection.close()

    return render_template('successful_account_update.html')
    
    

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/login", methods=["POST", "GET"])
@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == 'GET':
        return render_template("login.html", username="", error_message="")

    email = request.values.get("email")
    password = request.values.get("password")
    connection = sqlite3.connect(DATA_BASE_FILE_PATH)
    cur = connection.cursor()
    cur.execute("SELECT * FROM Accounts WHERE email=? and password=?", (email, password))
    one_user = cur.fetchone()

    if one_user is not None:
        # Put a new value into session
        session["logged_in_user"] = email
        connection.close()
        return redirect("/logged_in_confirmation")
    else:
        connection.close()
        return render_template("login.html", email=email, error_message="Email or password is wrong!")

@app.route('/logged_in_confirmation')
def logged_in_confirmation():
    return render_template('logged_in_confirmation.html')

@app.route("/logged_out", methods=["POST", "GET"])
def logout():
    session.clear()
    return render_template("successful_logout.html")

@app.route('/create_account')
def create_account():
    return render_template('create_account.html')

@app.route('/action_page', methods=["POST"])
def action_page():
    full_name = request.values.get('full_name')
    level = request.form["proficiency"]
    age = request.values.get('age')
    email = request.values.get('email')
    password = request.values.get('password')

    easter_egg = 'easter_egg'
    
    connection = sqlite3.connect(DATA_BASE_FILE_PATH)
    cur = connection.cursor()
    cur.execute(
        "INSERT INTO Accounts (full_name, level, age, email, password, previous_seven_subjects) VALUES (?, ?, ?, ?, ?, ?)",
        (full_name, level, age, email, password, easter_egg))
    connection.commit()
    connection.close()

    session["logged_in_user"] = email

    
    return render_template('successful_account_creation.html')


if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.debug = True
    app.run(host="0.0.0.0", port=5000, debug=True)