from flask import render_template, redirect, url_for, flash, request

import bcrypt

from config import session, USER
from app.auth import auth




USERNAME = 'Username'


# LOGIN ROUTE
@auth.route('/login', methods=['POST'])
def login():
  username = request.form['username']
  password = request.form['password']

  if verifyUser(username, password):
    return redirect('/home')
  
  return render_template('/auth/login.html', INVALID=True)


@auth.route('/', methods=['GET', 'POST'])
def index():
    return render_template('/auth/login.html')


def verifyUser(username, password):
    user = session.query(USER).filter_by(Username=username).first()
  
    if user and bcrypt.checkpw(password.encode('utf-8'), user.Password.encode('utf-8')):
        return True
    else:
        return False   




   