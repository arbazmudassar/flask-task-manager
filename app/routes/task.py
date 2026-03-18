from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from app import db
from app.models import Task

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/task_page')
def view_tasks():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    tasks = Task.query.filter_by(user_id=session['user']).all()
    return render_template('task.html', tasks=tasks)

@tasks_bp.route('/add', methods =["POST"])
def add_task():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    title = request.form.get('title')
    description = request.form.get('description')
    if title:
        new_task = Task(title=title, status='Pending', description=description, user_id=session['user'])
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully.', 'success')

    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/edit/<int:task_id>', methods=["GET", "POST"])
def edit(task_id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    task= Task.query.filter_by(user_id=session['user'],id=task_id).first()
    if not task:
        flash('Task not found','danger')
        return redirect(url_for('tasks.view_tasks'))
    
    if request.method == "POST":
        task.title=request.form.get('title')
        task.description=request.form.get('description')
        db.session.commit()
        flash('Task updated successfully','success')
        return redirect(url_for('tasks.view_tasks'))
    return render_template('edit.html',task=task)

@tasks_bp.route('/toggle/<int:task_id>', methods=["POST"])
def toggle_status(task_id):
    user = session.get('user')
    if not user:
        return redirect(url_for('auth.login'))
    
    task = Task.query.filter_by(user_id=user,id=task_id).first()
    if task:
        if task.status == 'Pending':
            task.status = 'Working'
        elif task.status == 'Working':
            task.status = 'Done'
        else:
            task.status = 'Done'
        db.session.commit()
        flash(f"Task '{task.title}' status updated to {task.status}.", "success")
    else:
        flash("Task not found or you are not the owner.", "danger")

    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/clear/<int:task_id>', methods=["POST"])
def clear_task(task_id):
    if task_id:
        Task.query.filter_by(user_id = session['user'], id=task_id).delete()
        db.session.commit()
        flash('Task deleted successfully.', 'info')
    else:
        Task.query.filter_by(user_id = session['user']).delete()
        db.session.commit()
        flash('All tasks cleared.', 'info')
    return redirect(url_for('tasks.view_tasks'))
