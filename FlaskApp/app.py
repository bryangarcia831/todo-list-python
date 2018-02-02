import parser
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from ConfigParser import SafeConfigParser, NoSectionError

app = Flask(__name__)

# dialect+driver://username:password@host:port/database
try:
    parser = SafeConfigParser()
    parser.read('../properties.ini')

    host = parser.get('aws-user-pw', 'host')
    user = parser.get('aws-user-pw', 'user')
    password = parser.get('aws-user-pw', 'password')
    database = parser.get('aws-user-pw', 'todo-database')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + user + ':' + password + \
                                            '@' + host + ':3306/' + database
except NoSectionError as err:
    print('You need the correct Properties file in your root directory')

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(52), nullable=False)
    lastName = db.Column(db.String(52), nullable=False)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dueDate = db.Column(db.TIMESTAMP, nullable=False)
    createdAt = db.Column(db.TIMESTAMP, nullable=False)
    createdBy = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text, nullable=True)


@app.route("/")
def main():
    bryan = User.query.filter_by(firstName='Bryan').first()
    todos = Todo.query.filter_by(createdBy=bryan.id).all()
    print bryan.firstName + ' ' + bryan.lastName
    if todos is not None:
        for todo in todos:
            print todo.text

    return render_template(
        'main-page.html', todos=todos)


if __name__ == "__main__":
    app.run()
