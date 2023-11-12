from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, Application
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password:
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password incorrect', category='error')
        else:
            flash('Email/Username does not exist', category='error')

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    flash('Logged out successfully', category='success')
    logout_user()
    return redirect(url_for('auth.login'))

#TODO: The new user has to have the default links for their account
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        pswd1 = request.form.get('password1')
        pswd2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('User already exists, please log in', category='error')
        elif pswd1 != pswd2:
            flash('Passwords do not match, please try again', category='error')
        else:
            new_user = User(email=email, password=pswd1)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created', category='success')
            # Hopefully this doesn't fuck shit up
            login_user(new_user, remember=True)
            active_apps = Application.query.filter(Application.status == True)
            cur_user = User.query.get(current_user.id)
            for a in active_apps:
                cur_user.links.append(a)
            db.session.commit()
            print('default links have been appended for the new user')
            return redirect(url_for('views.home'))
        
        
    return render_template('signup.html')