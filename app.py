from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask("MY-APPLICATION")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db' # mysql://user:password@host/database

db = SQLAlchemy(app)

class User(db.Model):
  __tablename__ = 'users'

  id = db.Column('id', db.Integer, primary_key = True)
  first_name = db.Column(db.String(50))
  last_name = db.Column(db.String(50))
  email = db.Column(db.String(50))

  def __init__(self, first_name, last_name, email):
     self.first_name = first_name
     self.email = email
     self.last_name = last_name

@app.route('/')
def show_all():
    return render_template("index.html", users = User.query.all())


@app.route('/user', methods=['POST', 'GET'])
def create_user():
    if request.method == 'GET':        
        return render_template("new.html")
    else:
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email =  request.form["email"]
        user = User(first_name, last_name, email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('show_all'))


if __name__ == '__main__':
    db.create_all()
    app.run()