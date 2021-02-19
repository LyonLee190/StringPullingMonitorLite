# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import random

from flask import jsonify, render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from app import db, login_manager
from app.base import blueprint
from app.base.forms import LoginForm, CreateAccountForm
from app.base.models import User, Experiments, Subjects, RealTimeData

from app.base.util import verify_pass

from datetime import datetime

## Dashboard

@blueprint.route('/index')
def render_index():
    return render_template('index.html')

@blueprint.route('/index', methods=['GET', 'POST'])
def get_training_para():
    if request.method == 'POST':
        experiment = Experiments()
        subject = Subjects()

        results = request.form
        experiment.experiment_id = results.get("experiment_ID")
        subject.subject_id = results.get("subject_ID")
        date = results.get("date")
        experiment.date = datetime.strptime(date, "%Y-%m-%d")
        experiment.duration = results.get("duration")
        experiment.comment = results.get("comment")

        experiment.required_force = float(results.get("input_force"))
        experiment.required_distance = float(results.get("input_distance"))
        experiment.allowable_time_window = float(results.get("input_time_window"))

        db.session.add(experiment)
        db.session.add(subject)
        db.session.commit()

        print("Experiment ID: %s, Subject ID: %s, Date: %s, Duration: %s, Comment: %s" % (experiment.experiment_id,
                                                                                          subject.subject_id,
                                                                                          date,
                                                                                          experiment.duration,
                                                                                          experiment.comment))
        print("Force: %.2f, distance: %.2f, time_window: %.2f" % (experiment.required_force,
                                                                  experiment.required_distance,
                                                                  experiment.allowable_time_window))
    return render_template('index.html')

@blueprint.route('/real_time_data_update', methods=["GET", "POST"])
def load_ajax():
    if request.method == 'POST':
        return jsonify(force_val=random.randint(0, 64),
                       velocity_val=random.randint(0, 64),
                       distance_val=random.randint(0, 32),
                       completions_val=random.randint(0, 16))

@blueprint.route('/sensor_data_update', methods=["GET", "POST"])
def retrieveSensorData():
    if request.method == 'POST':
        return jsonify(LC_val=random.randint(0, 64),
                       OS_1_val=random.randint(0, 64),
                       OS_2_val=random.randint(0, 64))

## Login & Registration

@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.login'))

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:
        
        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = User.query.filter_by(username=username).first()
        
        # Check the password
        if user and verify_pass( password, user.password):

            login_user(user)
            return redirect(url_for('base_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template( 'accounts/login.html', msg='Wrong user or password', form=login_form)

    if not current_user.is_authenticated:
        return render_template( 'accounts/login.html',
                                form=login_form)
    return redirect(url_for('home_blueprint.index'))

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    login_form = LoginForm(request.form)
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username  = request.form['username']
        email     = request.form['email'   ]

        # Check usename exists
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template( 'accounts/register.html', 
                                    msg='Username already registered',
                                    success=False,
                                    form=create_account_form)

        # Check email exists
        user = User.query.filter_by(email=email).first()
        if user:
            return render_template( 'accounts/register.html', 
                                    msg='Email already registered', 
                                    success=False,
                                    form=create_account_form)

        # else we can create the user
        user = User(**request.form)
        db.session.add(user)
        db.session.commit()

        return render_template( 'accounts/register.html', 
                                msg='User created please <a href="/login">login</a>', 
                                success=True,
                                form=create_account_form)

    else:
        return render_template( 'accounts/register.html', form=create_account_form)

@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('base_blueprint.login'))

@blueprint.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

## Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('page-403.html'), 403

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('page-403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('page-500.html'), 500
