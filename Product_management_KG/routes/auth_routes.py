from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.neo4j_user import Neo4jUser
import models.user as user_model  # handles Neo4j user creation & retrieval
import uuid

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# ----------------------- REGISTER -----------------------
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
            flash("Passwords do not match", "danger")
            return redirect(url_for('auth.register'))

        if user_model.get_user_by_email(email):
            flash("Email already registered", "danger")
            return redirect(url_for('auth.register'))

        user_id = str(uuid.uuid4())
        hashed_pw = generate_password_hash(password)
        user_model.create_user(user_id, name, email, hashed_pw, role, contact)
        flash("Registration successful! Please login.", "success")
        return redirect(url_for('auth.login'))

    return render_template('auth_templates/register.html')

# ------------------------ LOGIN -------------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user_node = user_model.get_user_by_email(email)
        if user_node:
            stored_password = user_node.get('password')
            if stored_password and check_password_hash(stored_password, password):
                user_obj = Neo4jUser(
                    id=user_node['id'],
                    name=user_node['name'],
                    email=user_node['email'],
                    role=user_node['role']
                )
                login_user(user_obj)
                flash('Login successful!', 'success')
                if user_obj.role == 'consumer':
                    return redirect(url_for('consumer.dashboard'))
                elif user_obj.role == 'supplier':
                    return redirect(url_for('supplier.dashboard'))
                elif user_obj.role == 'admin':
                    return redirect(url_for('admin.dashboard'))
        flash('Invalid email or password.', 'danger')
    return render_template('auth_templates/login.html')



# ------------------------ LOGOUT ------------------------
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/')
def home():
    return redirect(url_for('auth.login'))
