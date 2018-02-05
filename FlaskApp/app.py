import datetime

import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from ConfigParser import SafeConfigParser, NoSectionError
from passlib.hash import sha256_crypt

app = Flask(__name__, static_folder='../static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


# dialect+driver://username:password@host:port/database
try:
    parser = SafeConfigParser()
    parser.read('../properties.ini')

    host = parser.get('aws-user-pw', 'host')
    user = parser.get('aws-user-pw', 'user')
    password = parser.get('aws-user-pw', 'password')
    port = parser.get('aws-user-pw', 'port')
    database = parser.get('aws-user-pw', 'todo-database')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + user + ':' + password + \
                                            '@' + host + ':' + port + '/' + database
except NoSectionError as err:
    print('You need the correct Properties file in your root directory')

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(52), nullable=False)
    lastName = db.Column(db.String(52), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(256), nullable=False)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dueDate = db.Column(db.TIMESTAMP, nullable=False)
    createdAt = db.Column(db.TIMESTAMP, nullable=False)
    createdBy = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text, nullable=True)


@app.route("/")
@app.route("/home")
def main():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        # return render_template('login.html')
    else:
        bryan = User.query.filter_by(firstName='Bryan').first()
        todos = Todo.query.filter_by(createdBy=bryan.id).all()
        if todos is not None:
            f = '%B %d, %Y %I:%M %p'
            for todo in todos:
                todo.dueDateFormat = datetime.datetime.strftime(todo.dueDate, f)
                todo.createdAtFormat = datetime.datetime.strftime(todo.createdAt, f)
        return render_template(
            'main-page.html', todos=todos)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        pw = request.form['password']
        temp_user = User.query.filter_by(email=email).first()

        if not sha256_crypt.verify(pw, temp_user.password):
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('main'))
    return render_template('login.html', error=error)


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run()
