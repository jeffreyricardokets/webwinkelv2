from models import *
from flask import render_template, redirect, request, flash
import flask_login
from datetime import date
import bcrypt

salt = bcrypt.gensalt(rounds=8)

def create_user():
    #get the from data
    form_first_name = request.form.get('firstname')
    form_last_name = request.form.get('lastname')
    form_user_email = request.form.get('email')
    form_username = request.form.get('username')
    form_password = request.form.get('password')
    hashed_password = bcrypt.hashpw(form_password.encode('utf8'),salt)

    if user_exist(form_username):
        return 'User already exist'
    elif email_exists(form_user_email):
        return 'Email already exist'
    else:
        #create a user for our database
        Users.create(user_first_name = form_first_name,
        user_last_name = form_last_name,
        user_email_address = form_user_email,
        user_username = form_username,
        user_password = hashed_password,
        user_join_date = date.today(),
        is_authenticated = True,
        is_anonymous = False,
        is_active = True,
        is_admin = False)
        return 'user created'

    
def login_user():
    #get data from form
    form_username = request.form.get('username')
    form_password = request.form.get('password').encode('utf8')

    #check if username is in our database    
    if user_exist(form_username):
        user = Users.get(Users.user_username == form_username)
        encode_db_password = user.user_password.encode('utf8')
        if bcrypt.checkpw(form_password,encode_db_password):
            flask_login.login_user(user)
            return '/user/dashboard'
        else:
            return '/'
    else:
        return '/'

#check if user exist in our database
def user_exist(username):
    user_in_db = Users.select().where(Users.user_username == username)
    if user_in_db.exists():
        return True
    else:
        return False

#check if email adres exist
def email_exists(email):
    email_in_db = Users.select().where(Users.user_email_address == email)
    if email_in_db.exists():
        return True
    else:
        return False