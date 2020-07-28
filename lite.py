from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column('id', db.Integer, primary_key = True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

@app.route('/')
def hello():
    return render_template('hello.html', users = User.query.all())


@app.route('/user', methods=['POST', 'GET'])
def create_user():
    if request.method == 'GET':
        return render_template('reg.html')
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        user = User(first_name, last_name, email, password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('hello'))

if __name__ == '__main__':
    db.create_all()
    app.run()