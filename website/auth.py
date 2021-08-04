from flask import Blueprint, flash, redirect, render_template, request, url_for

from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .models import User

from flask_login import login_user, login_required,logout_user, current_user

auth = Blueprint('auth',__name__)

@auth.route('/login',methods=['GET','POST'])
def login():
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=email).first()
    
    if user:
      if check_password_hash(user.password,password):
        flash('Logged in successfully',category='success')
        login_user(user, remember=True)
        return redirect(url_for('views.home'))
      else:
        flash('Incorrect password',category='error')
    else:
      flash('No user found with specified email or username',category='error')
  return render_template('login.html',user=current_user)

@auth.route('/sign-up',methods=['GET','POST'])
def signUp():
  if request.method == 'POST':
    email = request.form.get('email')
    userName = request.form.get('userName')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    
    user_with_email = User.query.filter_by(email=email).first()
    user_with_name = User.query.filter_by(userName=userName).first()
    
    if user_with_email:
      flash('email already taken',category='error')
    elif user_with_name:
      flash('username taken',category='error')
    elif len(email) < 4:
      flash('Email must be greater than 4 characters.', category='error')
    elif len(userName) < 2:
      flash('Username must be greater than 2 or equal to 2 characters.', category='error')
    elif password1 != password2:
      flash('passwords do not match!',category='error')
    elif len(password1) < 7:
      flash('password should be greater than 7 characters')
    else:
      new_user = User(email=email,userName=userName,password=generate_password_hash(password1,method='sha256'))
      db.session.add(new_user)
      db.session.commit()
      login_user(new_user)
      flash('account created!',category='success')
      return redirect(url_for('views.home'))
  return render_template('signUp.html',user=current_user)

@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('auth.login'))
