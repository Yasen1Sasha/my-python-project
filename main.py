from flask import Flask, render_template, request, session, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
import os
from sqlalchemy import False_

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'school.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'FCqoCBhVqQ3CUZ5Cz6ez2cO0zujqJ15KoYslJNQwx8s'
db = SQLAlchemy(app)


class User:
   __tablename__= 'User'
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(50), nullable=False)
   email = db.Column(db.String(150), nullable=False, unique=True)
   password = db.Column(db.String(128), nullable=False)
   role = db.Column(db.Integer, default=0)

   def check_password(self, password):
      return check_password_hash(self.password, password)


@app.route('/')
def index():
   return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
      message = ''
      email = request.form['email']
      password = request.form['password']

      user = User.query.filter_by(email=email).first()

      if not user:
          message = 'Ти що припух, Введи правельний пароль! '
          return render_template('login.html', message='')
      else:
         if not user.check_password(password):
            session['user_name'] = user.username
            return redirect('/')

           message = 'Ти що припух, Введи правельний пароль! '

   return render_template('login.html', message='')


if __name__=='__main__':
   app.run(debug=True)