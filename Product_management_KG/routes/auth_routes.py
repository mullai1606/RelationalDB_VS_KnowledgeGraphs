from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import user  # user.py with get_user_by_email, create_user
from extensions import neo4j_driver

import uuid

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user_obj = user.get_user_by_email(email)

        if user_obj and check_password_hash(user_obj.password, password):
            login_user(user_obj)
            flash('Login successful!', 'success')

            if user_obj.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user_obj.role == 'supplier':
                return redirect(url_for('supplier.dashboard'))
            elif user_obj.role == 'consumer':
                return redirect(url_for('consumer.dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('auth_templates/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role']
        contact = request.form.get('contact', '')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('auth.register'))

        if user.get_user_by_email(email):
            flash('Email already registered.', 'danger')
            return redirect(url_for('auth.register'))

        hashed_pw = generate_password_hash(password)
        user_id = str(uuid.uuid4())

        # Save user in Neo4j
        user.create_user(
            user_id=user_id,
            name=name,
            email=email,
            password=hashed_pw,
            role=role,
            contact=contact
        )

        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth_templates/register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/')
def home():
    return redirect(url_for('auth.login'))
