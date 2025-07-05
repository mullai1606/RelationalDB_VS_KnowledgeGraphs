from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.neo4j_user import Neo4jUser
import models.user as user_model  # handles Neo4j user creation & retrieval
import uuid
from extensions import neo4j_driver

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# ----------------------- REGISTER -----------------------
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('username')
        email = request.form['email']
        contact = request.form.get('contact', '')
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        selected_roles = request.form.getlist('roles')  # ✅ Handles multiple roles

        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return redirect(url_for('auth.register'))

        if user_model.get_user_by_email(email):
            flash("Email already registered", "danger")
            return redirect(url_for('auth.register'))

        user_id = str(uuid.uuid4())
        hashed_pw = generate_password_hash(password)

        # ✅ Create User node
        user_model.create_user(user_id, name, email, hashed_pw, "", contact)

        with neo4j_driver.session() as session:
            for role in selected_roles:
                # ✅ Create Role node if not exists
                session.run("""
                    MERGE (r:Role {name: $role})
                """, role=role)

                # ✅ Create relationship: (User)-[:HAS_ROLE]->(Role)
                session.run("""
                    MATCH (u:User {id: $user_id}), (r:Role {name: $role})
                    MERGE (u)-[:HAS_ROLE]->(r)
                """, user_id=user_id, role=role)

        flash("Registration successful! Please login.", "success")
        return redirect(url_for('auth.login'))

    return render_template('auth_templates/register.html')


# ------------------------ LOGIN -------------------------
# @auth_bp.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         user_node = user_model.get_user_by_email(email)
#         if user_node:
#             stored_password = user_node.get('password')
#             if stored_password and check_password_hash(stored_password, password):
#                 user_obj = Neo4jUser(
#                     id=user_node['id'],
#                     name=user_node['name'],
#                     email=user_node['email'],
#                     role=user_node['role']
#                 )
#                 login_user(user_obj)
#                 flash('Login successful!', 'success')
#                 if user_obj.role == 'consumer':
#                     return redirect(url_for('consumer.dashboard'))
#                 elif user_obj.role == 'supplier':
#                     return redirect(url_for('supplier.dashboard'))
#                 elif user_obj.role == 'admin':
#                     return redirect(url_for('admin.dashboard'))
#         flash('Invalid email or password.', 'danger')
#     return render_template('auth_templates/login.html')

#commented for multi role user support 

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user_node = user_model.get_user_by_email(email)

        if user_node:
            stored_password = user_node.get('password')

            if stored_password and check_password_hash(stored_password, password):
                # Extract roles from user_node['roles'] list of dicts
                role_nodes = user_node.get('roles', [])
                role_names = [role['name'] for role in role_nodes]

                user_obj = Neo4jUser(
                    id=user_node.get('id'),
                    name=user_node.get('name'),
                    email=user_node.get('email'),
                    roles=role_names
                )

                login_user(user_obj)

                if len(role_names) > 1:
                    return redirect(url_for('auth.select_role'))
                else:
                    role = role_names[0]
                    if role == 'admin':
                        return redirect(url_for('admin.dashboard'))
                    elif role == 'supplier':
                        return redirect(url_for('supplier.dashboard'))
                    elif role == 'consumer':
                        return redirect(url_for('consumer.dashboard'))

        flash('Invalid email or password.', 'danger')

    return render_template('auth_templates/login.html')


# ------------------------ role selection ------------------------
@auth_bp.route('/select_role', methods=['GET', 'POST'])
@login_required
def select_role():
    if request.method == 'POST':
        selected_role = request.form.get('selected_role')

        if selected_role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif selected_role == 'supplier':
            return redirect(url_for('supplier.dashboard'))
        else:
            # Default to consumer dashboard for any other role
            return redirect(url_for('consumer.dashboard'))

        flash('Invalid role selected.', 'danger')

    # ✅ Ensure roles are string list (not dicts)
    roles = [r['name'] if isinstance(r, dict) else r for r in current_user.roles]
    return render_template('auth_templates/select_role.html', roles=roles)



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
