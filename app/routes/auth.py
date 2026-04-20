from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import db
from datetime import datetime

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password) and user.is_active:
            login_user(user, remember=bool(remember))
            user.last_login = datetime.utcnow()
            db.session.commit()
            next_page = request.args.get('next')
            if user.role == 'admin':
                return redirect(next_page or url_for('admin.dashboard'))
            elif user.role == 'doctor':
                return redirect(next_page or url_for('doctor.dashboard'))
            else:
                return redirect(next_page or url_for('patient.dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('auth/login.html', config=current_app.config)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html', config=current_app.config)

        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please login.', 'warning')
            return redirect(url_for('auth.login'))

        username = email.split('@')[0]
        base_username = username
        counter = 1
        while User.query.filter_by(username=username).first():
            username = f"{base_username}{counter}"
            counter += 1

        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            role='patient'
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f'Welcome, {first_name}! Your account has been created.', 'success')
        return redirect(url_for('patient.dashboard'))
    return render_template('auth/register.html', config=current_app.config)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.index'))

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.first_name = request.form.get('first_name', current_user.first_name)
        current_user.last_name = request.form.get('last_name', current_user.last_name)
        current_user.phone = request.form.get('phone', current_user.phone)
        current_user.address = request.form.get('address', current_user.address)
        db.session.commit()
        flash('Profile updated successfully.', 'success')
    return render_template('auth/profile.html', config=current_app.config)
