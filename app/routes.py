from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Logs


@app.route('/')
@app.route('/index')
def index():
    username = None
    if current_user is not None and current_user.is_authenticated:
        username = current_user.username
    return render_template('index.html', username=username)


@app.route('/public')
def public():
    return render_template('public.html')


@app.route('/private')
def private():
    if current_user is not None and current_user.is_authenticated:
        return render_template('private.html')
    return render_template('denied.html')


@app.route('/secret')
def secret():
    if current_user is not None and current_user.is_authenticated:
        # if admin
        if current_user.role is 0:
            return render_template('secret.html')
    return render_template('denied.html')


@app.route('/logs')
def logs():
    if current_user is not None and current_user.is_authenticated:
        # if admin
        if current_user.role is 0:
            records = get_registered_records()
            return render_template('log_template.html', records=records)
    return render_template('denied.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            if user is not None:
                log_action(user, action="Login Failed")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        log_action(user, action="Login Successful")
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        log_action(user, action="Registration")
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


def log_action(user, action: str = "something"):
    log = Logs(user_id=user.id, username=user.username, action=action)
    db.session.add(log)
    db.session.commit()


def get_registered_records():
    logs = Logs.query.all()
    records = []
    for log in logs:
        record = {
            'username': log.username,
            'date_time': log.timestamp,
            'action': log.action
        }
        records.append(record)
    return records
