from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import re
import subprocess as s
import secrets
import mysql.connector
try :
    import data_generator as dg
except Exception as e :
    pass
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd

main_data = {}
app = Flask(__name__)
app.secret_key = secrets.token_hex(24)

def generate_query(prompt):
    try:
        f = open ( "maindata.txt")
        data = f.read()
        f.close()
        command = "ollama run llama3.2 \\Analyze the following database details, including table names, column names, data types, relationships, and any additional constraints provided. Based on this analysis, generate a MySQL query that meets the described requirements. Ensure the query adheres to standard SQL syntax and focuses on clarity, accuracy, and efficiency. Only provide the MySQL query as output, without any explanatory text or additional commentary , dont enclose with string unless it is a specific value . always specify their database name while selecting tables .{0} and the question is : {1}".format(data ,prompt)
        result =s.run(command, shell=True, capture_output=True, text=True)
        cleaned_output = result.stdout.strip()
        f1 = open("query.txt","w")
        f1.write(cleaned_output)
        f1.close()
        return cleaned_output
    except UnicodeDecodeError as e:
        pass
def connect_to_database():
    try:
        with open("data_folder/dbdata.txt", "r") as file:
            data = eval(file.read())
        conn = mysql.connector.connect(
            host=data['host'],
            user=data['username'],
            password=data['password']
        )
        return conn if conn.is_connected() else None
    except (mysql.connector.Error, FileNotFoundError, SyntaxError):
        return None
def fetch_user_data():
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("USE talkdb;")
            cursor.execute("SELECT * FROM login_details;")
            return [{"username": row[0], "password": row[1]} for row in cursor.fetchall()]
        finally:
            conn.close()
    return []


user_datas = fetch_user_data()


def is_valid_password(password):
    return len(password) >= 8 and all([
        re.search(r'[A-Z]', password),
        re.search(r'[a-z]', password),
        re.search(r'[0-9]', password),
        re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
    ])


@app.route('/')
def signin():
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global db_password , db_host , db_username
    if request.method == 'POST':
        db_host = request.form.get('db_host')
        db_password = request.form.get('db_password')
        db_username = request.form.get('db_username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get("email")
        password = request.form.get('password')
        repassword = request.form.get('retype_password')
        if not all([first_name, last_name, email, password, repassword]):
            flash("All fields are required!", category="error")
            return redirect('/signup')
        if password != repassword:
            flash("Passwords do not match!", category="error")
            return redirect('/signup')
        if not is_valid_password(password):
            flash("Password must meet complexity requirements.", category="error")
            return redirect('/signup')
        conn = connect_to_database()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("CREATE DATABASE IF NOT EXISTS talkdb;")
                cursor.execute("USE talkdb;")
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS user_details ("
                    "email VARCHAR(100) NOT NULL PRIMARY KEY,"
                    "firstname VARCHAR(100),"
                    "lastname VARCHAR(100)"
                    ");"
                )
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS login_details ("
                    "email VARCHAR(100) NOT NULL PRIMARY KEY,"
                    "password VARCHAR(255),"
                    "FOREIGN KEY (email) REFERENCES user_details(email)"
                    ");"
                )
                hashed_password = generate_password_hash(password)
                cursor.execute(
                    "INSERT INTO user_details (email, firstname, lastname) VALUES (%s, %s, %s)",
                    (email, first_name, last_name)
                )
                cursor.execute(
                    "INSERT INTO login_details (email, password) VALUES (%s, %s)",
                    (email, hashed_password)
                )
                conn.commit()
                flash("Signup successful! Please log in.", category="success")
                return redirect('/')
            except mysql.connector.Error as e:
                flash(f"Database error: {e}", category="error")
            except Exception as e:
                flash(f"An error occurred: {e}", category="error")
            finally:
                conn.close()
        else:
            flash("Database connection error!", category="error")
            return redirect('/signup')
    return render_template('signup.html')

@app.route('/frontpage')
def frontpage():
    if "user" not in session:
        return redirect(url_for("signin"))
    return render_template("frontpage.html")


@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get("username")
    password = request.form.get("password")

    for user in user_datas:
        if user["username"] == username and check_password_hash(user["password"], password):
            session["user"] = username
            return redirect(url_for("frontpage"))

    flash("Invalid credentials! Please try again.", "error")
    return redirect(url_for("signin"))
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if "user" not in session:
        return redirect(url_for("signin"))
    if request.method == 'POST':
        current_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not check_password_hash(user_datas.get("password", ""), current_password):
            flash("Current password is incorrect!", category="error")
            return redirect(url_for('change_password'))

        if new_password != confirm_password:
            flash("New passwords do not match!", category="error")
            return redirect(url_for('change_password'))

        if not is_valid_password(new_password):
            flash("New password must meet complexity requirements.", category="error")
            return redirect(url_for('change_password'))

        conn = connect_to_database()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("USE talkdb;")
                hashed_password = generate_password_hash(new_password)
                cursor.execute("UPDATE login_details SET password = %s WHERE email = %s", (hashed_password, user_datas["username"]))
                conn.commit()
                user_datas["password"] = hashed_password
                flash("Password updated successfully!", category="success")
                return redirect(url_for('signin'))
            finally:
                conn.close()
    return render_template('change_password.html')
@app.route('/get_data')
def get_data():
    global main_data
    data = dg.main()
    with open("maindata.txt", "r") as file:
        main_data = eval(file.read())
        return jsonify(data)
@app.route('/configure_database', methods=['POST'])
def configure_database():
    db_username = request.form.get('db_username')
    db_password = request.form.get('db_password')
    db_host = request.form.get('db_host')

    if not all([db_username, db_password, db_host]):
        flash("All fields are required!", category="error")
        return redirect(url_for("frontpage"))

    db_data = {'username': db_username, 'password': db_password, 'host': db_host}
    with open("data_folder/dbdata.txt", "w") as file:
        file.write(str(db_data))

    data = dg.main()
    file = open("data.txt","w")
    file.write(str(data))
    file.close()
    with open("maindata.txt", "w") as file:
        file.write(str(data))

    flash("Database details configured successfully!", category="success")
    return redirect(url_for("frontpage"))
@app.route('/logout')
def logout():
    session.pop("user", None)
    flash("Logged out successfully!", category="success")
    return redirect(url_for("signin"))

@app.route('/process_query', methods=['POST'])
def process_query():
    data = request.get_json()
    query = data.get("query")
    sql_query = generate_query(query) 
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql_query)
            mysql_data = [row for row in cursor.fetchall()]
            return jsonify({
                "success": True,
                "message": f"Natural Language Processed Query: \n '{sql_query}'",
                "query_result": mysql_data
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "message": f"Natural Language Processed Query: \n '{sql_query}'",
                "query_result": f"Error executing SQL query: {e}"
            })
        finally:
            conn.close()

    return jsonify({
        "success": False,
        "message": "Database connection error.",
        "query_result": []
    })
if __name__ == "__main__":
    app.run(debug=True) 
