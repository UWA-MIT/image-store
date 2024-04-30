# Importing necessary modules and classes from Flask and other libraries
from flask import render_template, flash, redirect, url_for, request, current_app
from urllib.parse import urlsplit
import sqlalchemy as sa
from datetime import timedelta

# Importing necessary modules and classes from the application
from app import db
from app.auth import bp
from app.models.user import User
from app.models.reward import Reward

# Importing necessary functions and classes from Flask-Login for user authentication
from flask_login import current_user, login_user, logout_user, login_required
from app.auth.forms import LoginForm, RegistrationForm, ChangePasswordForm, \
        ResetPasswordRequestForm, ResetPasswordForm

# Importing the send_password_reset_email function from the email module
from app.email import send_password_reset_email

# Route for user login
@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Redirects user to index if already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    # Form instantiation
    form = LoginForm()
    
    # Form validation and processing
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data, duration=timedelta(days=current_app.config['REMEMBER_ME_DAYS']))
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Sign In', form=form)


# Route for user logout
@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


# Route for user registration
@bp.route('/register', methods=['GET', 'POST'])
def register():
    # Redirects user to index if already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    # Form instantiation
    form = RegistrationForm()
    
    # Form validation and processing
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, name=form.name.data, status='Active')
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        # Add reward for user registration.
        Reward.addRewardForRegistration(user.id)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Register', form=form)


# Route for changing user password
@bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    # Form instantiation with current user's username
    form = ChangePasswordForm(current_user.username)
    
    # Form validation and processing
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == current_user.username))
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been changed.')
        return redirect(url_for('auth.change_password'))
    
    return render_template('auth/change_password.html', title='Change password', form=form)


# Route for requesting password reset
@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    # Redirects user to index if already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    
    # Form instantiation
    form = ResetPasswordRequestForm()
    
    # Form validation and processing
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.email == form.email.data))
        if user:
            send_password_reset_email(user)
            flash('Check your email for the instructions to reset your password')
            return redirect(url_for('auth.login'))
        else:
            flash('The email address you provided is not registered.')
    
    return render_template('auth/reset_password_request.html', title='Reset Password', form=form)


# Route for resetting password
@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # Redirects user to index if already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    # Verifies reset password token
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    
    # Form instantiation
    form = ResetPasswordForm()
    
    # Form validation and processing
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', form=form)
