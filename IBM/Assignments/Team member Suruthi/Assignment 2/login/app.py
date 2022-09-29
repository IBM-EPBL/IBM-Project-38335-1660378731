from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
 
app.secret_key = 'your secret key'
 
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ibm_db'
 
mysql = MySQL(app)

@app.route('/')
# @app.route('/login')
# def login():
#     return render_template('login.html')
# @app.route('/index')
# def index():
#     return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = % s AND password = % s', (email, password, ))
        account = cursor.fetchone()
        if account:
            # session['loggedin'] = True
            # session['id'] = account['id']
            # session['email'] = account['email']
            msg = 'Logged in successfully !'
            return render_template('dashboard.html', msg=msg,email=email)
        else:
            msg = 'Incorrect email / password !'
            return render_template('login.html', msg = msg)
    else:
        return render_template('login.html')
 

@app.route('/index', methods =['GET', 'POST'])
def index():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
            return render_template('index.html',msg=msg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not email or not password:
            msg = 'Please fill out the form !'
            return render_template('index.html',msg=msg)
        else:
            cursor.execute('INSERT INTO accounts(email,password) VALUES (email,password)')
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            return render_template('dashboard.html', msg = msg,email=email)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
        return render_template('index.html',msg=msg)
    else:
        return render_template('index.html')

