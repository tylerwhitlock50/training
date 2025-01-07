import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user
from app.extensions import db, login_manager
from app.models import User
from app.blueprints.auth import auth_bp
from app.blueprints.auth.forms import LoginForm, LogoutForm


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login Successful!', 'success')
            return redirect(url_for('default.index'))
        else:
            flash('Login Failed!', 'danger')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST']) 
def register():
    return 'Register'

@auth_bp.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))