from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from app import db, login_manager
from models.user import User, Consumer
from models.supplier import Supplier

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if not user:
            flash('User not found. Please register.', 'warning')
            return redirect(url_for('auth.login'))

        if not check_password_hash(user.password, password):
            flash('Incorrect password. Please try again.', 'danger')
            return redirect(url_for('auth.login'))

        login_user(user)
        flash('Logged in successfully.', 'success')
        return redirect(url_for(f'{user.role}.dashboard'))  # Redirect based on role

    return render_template('auth_templates/login.html')


# @auth_bp.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         role = request.form['role']
#         name = request.form['username']
#         email = request.form['email']
#         contact = request.form.get('contact', '')
#         password = request.form['password']
#         confirm_password = request.form['confirm_password']

#         # Check if email already exists
#         if User.query.filter_by(email=email).first():
#             flash('Email already registered. Please login or use a different email.', 'danger')
#             return redirect(url_for('auth.register'))

#         # Check if passwords match
#         if password != confirm_password:
#             flash('Passwords do not match. Please try again.', 'danger')
#             return redirect(url_for('auth.register'))

#         hashed_password = generate_password_hash(password)
#         user = User(role=role, name=name, email=email, contact=contact, password=hashed_password)
#         db.session.add(user)
#         db.session.commit()
#         flash('Registration successful. Please login.', 'success')
#         return redirect(url_for('auth.login'))

#     return render_template('auth_templates/register.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        role = request.form['role']
        name = request.form.get('username')
        email = request.form['email']
        contact = request.form.get('contact', '')
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please login or use a different email.', 'danger')
            return redirect(url_for('auth.register'))

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password)
        user = User(role=role, name=name, email=email, contact=contact, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        # ✅ Automatically create linked entries in Supplier/Consumer tables
        if role == 'supplier':
            supplier = Supplier(id=user.id, name=name, email=email, contact=contact)
            db.session.add(supplier)
            db.session.commit()

        elif role == 'consumer':
            consumer = Consumer(id=user.id, name=name, email=email, contact=contact, password=hashed_password)
            db.session.add(consumer)
            db.session.commit()

        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth_templates/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
