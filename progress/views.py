# -*- coding: utf-8 -*-
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from progress import app, db
from progress.models import User, Project


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))

        title = request.form['title']
        total = request.form['total']
        progress = request.form['progress']
        percent = "%.2f%%" % round(int(progress)/int(total)*100, 2)

        if not title or not total or not progress:
            flash('Invalid input.')
            return redirect(url_for('index'))

        project = Project(title=title, total=total, progress=progress, percent=percent)
        db.session.add(project)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('index'))

    projects = Project.query.all()
    return render_template('index.html', projects=projects)


@app.route('/project_id/edit/<int:project_id>', methods=['GET', 'POST'])
@login_required
def edit(project_id):
    project = Project.query.get_or_404(project_id)

    if request.method == 'POST':
        title = request.form['title']
        total = request.form['total']
        progress = request.form['progress']

        if not title or not total or not progress:
            flash('Invalid input.')
            return redirect(url_for('edit', project_id=project_id))

        project.title = title
        project.total = int(total)
        project.progress = int(progress)
        project.percent = "%.2f%%" % round(int(progress)/int(total)*100, 2)
        db.session.commit()
        flash('Item updated.')
        return redirect(url_for('index'))

    return render_template('edit.html', project=project)


@app.route('/project_id/update/<int:project_id>', methods=['GET', 'POST'])
@login_required
def update(project_id):
    project = Project.query.get_or_404(project_id)

    if request.method == 'POST':
        progress = request.form['progress']

        if not progress:
            flash('Invalid input.')
            return redirect(url_for('update', project_id=project_id))

        project.progress = int(progress)
        project.percent = "%.2f%%" % round(int(progress)/project.total*100, 2)
        db.session.commit()
        flash('Item updated.')
        return redirect(url_for('index'))

    return render_template('update.html', project=project)


@app.route('/project_id/delete/<int:project_id>', methods=['POST'])
@login_required
def delete(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        user = User.query.first()
        user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()

        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login success.')
            return redirect(url_for('index'))

        flash('Invalid username or password.')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('register'))

        user = User.query.first()

        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login success.')
            return redirect(url_for('index'))

        flash('Invalid username or password.')
        return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))
