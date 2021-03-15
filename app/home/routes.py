# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import jsonify, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager

from jinja2 import TemplateNotFound

from app import db, login_manager
from app.base.models import User, Configure, Experiment, Subject, RealTimeData

from datetime import datetime
import random


@blueprint.route('/index')
@login_required
def index():
    return render_template('index.html', segment='index')


@blueprint.route('/configure')
@login_required
def configure():
    return render_template('ui-configure.html')


# upload experiment info
@blueprint.route('/configure/upload/experiment_info', methods=['GET', 'POST'])
@login_required
def configure_submit():
    if request.method == 'POST':
        try:
            exp_info = Experiment()
            exp_info.id = request.form["experiment_id"]

            subject = Subject()
            subject.id = request.form["subject_id"]

            exp_info.date = datetime.strptime(request.form["date"], "%Y-%m-%d")
            exp_info.duration = int(request.form["duration"])
            exp_info.comment = request.form["comment"]
            exp_info.configure_id = int(request.form["setting_id"])

            db.session.merge(exp_info)
            db.session.merge(subject)
            db.session.commit()

            return jsonify(msg="Experiment Info Submitted")
        except ValueError:  # empty input
            return jsonify(msg="ValueError")


# upload training configuration
@blueprint.route('/configure/upload/configuration', methods=['GET', 'POST'])
@login_required
def configure_upload():
    if request.method == 'POST':
        try:
            train_configure = Configure()
            train_configure.id = int(request.form["setting_id"])
            train_configure.required_force = float(request.form["input_force"])
            train_configure.required_distance = float(request.form["input_distance"])
            train_configure.allowable_time_window = float(request.form["input_time_window"])

            db.session.merge(train_configure)
            db.session.commit()

            return jsonify(msg="Training Setting Uploaded")
        except ValueError:  # empty input
            return jsonify(msg="ValueError")

# query the saved configuration
@blueprint.route('/configure/query/configuration', methods=['GET', 'POST'])
@login_required
def configure_query():
    if request.method == 'POST':
        configure_id = int(request.form["setting_id"])
        train_configure = db.session.query(Configure).get(configure_id)
        if train_configure is None:
            train_configure = Configure()
            train_configure.id = configure_id

            db.session.merge(train_configure)
            db.session.commit()

        return jsonify(input_force=train_configure.required_force,
                       input_distance=train_configure.required_distance,
                       input_time_window=train_configure.allowable_time_window)


@blueprint.route('/database')
@login_required
def database():
    subject_col = db.session.query(Subject.id).distinct()
    return render_template('ui-database.html', subject_col=subject_col)


# query the saved experiment record for a given training subject
@blueprint.route('/database/query/experiment_id', methods=['GET', 'POST'])
@login_required
def experiment_query():
    if request.method == 'POST':
        subject_id = request.form["subject_id"]
        experiment_id = db.session.query(RealTimeData.experiment_id)\
            .filter(RealTimeData.subject_id.in_([subject_id]))\
            .distinct()\
            .all()
        
        return jsonify(experiment_id=experiment_id)


# @blueprint.route('/index', methods=['GET', 'POST'])
# @login_required
# def get_training_para():
#     if request.method == 'POST':
#         experiment = Experiments()
#         subject = Subjects()
#
#         results = request.form
#         experiment.experiment_id = results.get("experiment_ID")
#         subject.subject_id = results.get("subject_ID")
#         date = results.get("date")
#         experiment.date = datetime.strptime(date, "%Y-%m-%d")
#         experiment.duration = results.get("duration")
#         experiment.comment = results.get("comment")
#
#         experiment.required_force = float(results.get("input_force"))
#         experiment.required_distance = float(results.get("input_distance"))
#         experiment.allowable_time_window = float(results.get("input_time_window"))
#
#         db.session.add(experiment)
#         db.session.add(subject)
#         db.session.commit()
#
#         print("Experiment ID: %s, Subject ID: %s, Date: %s, Duration: %s, Comment: %s" % (experiment.experiment_id,
#                                                                                           subject.subject_id,
#                                                                                           date,
#                                                                                           experiment.duration,
#                                                                                           experiment.comment))
#         print("Force: %.2f, distance: %.2f, time_window: %.2f" % (experiment.required_force,
#                                                                   experiment.required_distance,
#                                                                   experiment.allowable_time_window))
#     return render_template('index.html')
#
# @blueprint.route('/real_time_data_update', methods=["GET", "POST"])
# def load_ajax():
#     if request.method == 'POST':
#         return jsonify(force_val=random.randint(0, 64),
#                        velocity_val=random.randint(0, 64),
#                        distance_val=random.randint(0, 32),
#                        completions_val=random.randint(0, 16))
#
# @blueprint.route('/sensor_data_update', methods=["GET", "POST"])
# def retrieveSensorData():
#     if request.method == 'POST':
#         return jsonify(LC_val=random.randint(0, 64),
#                        OS_1_val=random.randint(0, 64),
#                        OS_2_val=random.randint(0, 64))


@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template(template, segment=segment)

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except:
        return render_template('page-500.html'), 500


# Helper - Extract current page name from request 
def get_segment(request):
    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
