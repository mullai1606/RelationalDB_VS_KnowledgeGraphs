from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app import db, login_manager
from models.user import User, Consumer
from models.supplier import Supplier
from models.role import user_role
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# @auth_bp.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         user = User.query.filter_by(email=email).first()

#         if not user:
#             flash('User not found. Please register.', 'warning')
#             return redirect(url_for('auth.login'))

#         if not check_password_hash(user.password, password):
#             flash('Incorrect password. Please try again.', 'danger')
#             return redirect(url_for('auth.login'))

#         login_user(user)
#         flash('Logged in successfully.', 'success')
#         return redirect(url_for(f'{user.roles}.dashboard'))  # Redirect based on role

#     return render_template('auth_templates/login.html')


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

from models.role import Role  # Make sure you have a Role model
from sqlalchemy import insert

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('username')
        email = request.form['email']
        contact = request.form.get('contact', '')
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        selected_roles = request.form.getlist('roles')  # <-- multiple roles

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please login or use a different email.', 'danger')
            return redirect(url_for('auth.register'))

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password)
        user = User(name=name, email=email, contact=contact, password=hashed_password)

        # Add roles to user
        for role_name in selected_roles:
            role = Role.query.filter_by(name=role_name).first()
            if role:
                user.roles.append(role)
            else:
                # Optionally create role if it doesn't exist
                new_role = Role(name=role_name)
                db.session.add(new_role)
                db.session.flush()  # get ID without committing
                user.roles.append(new_role)

        db.session.add(user)
        db.session.commit()

        # Add to supplier or consumer table if applicable
        if 'supplier' in selected_roles:
            supplier = Supplier(id=user.id, name=name, email=email, contact=contact)
            db.session.add(supplier)
        if 'consumer' in selected_roles:
            consumer = Consumer(id=user.id, name=name, email=email, contact=contact, password=hashed_password)
            db.session.add(consumer)

        db.session.commit()

        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth_templates/register.html')

from flask import session

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            session['user_id'] = user.id

            # Get all role names (e.g., ['admin', 'supplier'])
            roles = [r.name for r in user.roles]

            if len(roles) == 1:
                # Redirect based on the single role
                role = roles[0]
                if role == 'admin':
                    return redirect(url_for('admin.dashboard'))
                elif role == 'supplier':
                    return redirect(url_for('supplier.dashboard'))
                else:
                    return redirect(url_for('consumer.dashboard'))
            else:
                # Redirect to role selector
                return redirect(url_for('auth.select_role'))

        flash("Invalid email or password", "danger")
    return render_template('auth_templates/login.html')


@auth_bp.route('/select-role', methods=['GET', 'POST'])
@login_required
def select_role():
    roles = [r.name for r in current_user.roles]

    if request.method == 'POST':
        selected_role = request.form['selected_role']
        if selected_role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif selected_role == 'supplier':
            return redirect(url_for('supplier.dashboard'))
        else:
            return redirect(url_for('consumer.dashboard'))

    return render_template('auth_templates/select_role.html', roles=roles)


@auth_bp.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for('auth.login'))
