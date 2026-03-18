from app import db
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import Users

auth_bp = Blueprint('auth', __name__)
task_bp = Blueprint('tasks', __name__)

@auth_bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            username = request.form.get('username')
            password = request.form.get('password')
        

            if username and password:
                new_user = Users(username=username, password=password)
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('auth.login'))
        except Exception as e:
            flash('Please Enter Unique and valid username or password.', 'danger')
            return redirect(url_for('auth.register'))
    
    return render_template('register.html')

@auth_bp.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        user = Users.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user'] = username
            flash('Login Successful', 'success')
            return redirect(url_for('tasks.view_tasks'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/delete')
def delete():
    Users.query.filter_by(username=session['user']).delete()
    db.session.commit()
    session.pop('user',None)
    flash('Account Deleted Successfully', 'info')
    return render_template('login.html')