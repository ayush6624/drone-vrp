from final import main
from functools import wraps
import sys
from datetime import datetime, timedelta
import bcrypt
import os
from flask import Flask, render_template, url_for, send_from_directory, request, session, redirect, flash, jsonify

app = Flask(__name__)
b = os.environ.get("FLASK_SECRET_KEY")
app.secret_key = b  # Use Env variable


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'email' in session:
            return f(*args, **kwargs)
        else:
            flash("Login First!")
            return(redirect("/accounts"))
    return wrap


@app.route('/')
def index():
    '''Returns the homepage'''
    return render_template('index.html')


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/submit', methods=['POST'])
def submit():
    body = request.json
    coord = []
    for i in body['coordinates']:
        coord.append([i['lat'], i['lng']])
    main(coord)
    return jsonify({"recevied": True})

# Account management


@app.route('/accounts')
def show_login():
    '''Show login page'''
    return render_template("accounts.html")


@app.route('/accounts/<action>', methods=['POST', 'GET'])
def login(action):
    '''Login API Endpoint using POST'''
    if(action == "login"):
        if request.method == 'POST':
            email = request.form["login"]  # use #name value here
            password = request.form["password"]
            users = mongo.udemy.users
            login_user = users.find_one({"email": email})

            if login_user:
                # no need to encode it as already in bytes
                orig_pass = login_user['password']
                if bcrypt.hashpw(password.encode('utf-8'), orig_pass) == orig_pass:
                    session['email'] = email
                    return redirect('/')
                return "Invalid username/password combination"
            return "invalid username"
        elif request.method == 'GET':
            return render_template('accounts.html')
    if (action == "signup"):
        if request.method == 'POST':
            email = request.form["signup_email"]  # use #name value here
            return render_template("signup.html", email=email)


@app.route('/assets/<path:path>')
def assets(path):
    '''Serve static content for the homepage'''
    return send_from_directory('templates', path)


@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash("Successfully Logged out")
    return redirect(url_for('index'))


@app.route('/accounts/signup/new', methods=['POST', 'GET'])
def new_user():
    if request.method == 'POST':
        users = mongo.udemy.users
        existing_user = users.find_one({'email': request.form['login']})
        if existing_user is None:
            hashpass = bcrypt.hashpw(
                request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert(
                {'email': request.form['login'], 'password': hashpass})
            session['email'] = request.form['login']
            return redirect(url_for('index'))
        return "already exists"
    return redirect('index')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', threaded=True)
