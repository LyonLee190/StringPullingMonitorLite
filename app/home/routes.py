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

from .manager import Manager

# global variables
train_configure = Configure()
manager = Manager()


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
def upload_experiment_info():
    global train_configure
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

            manager.execute(exp_info, subject, train_configure)

            return jsonify(msg="Training Completed")
        except ValueError:  # empty input
            return jsonify(msg="ValueError")


# upload training configuration
@blueprint.route('/configure/upload/configuration', methods=['GET', 'POST'])
@login_required
def upload_configuration():
    global train_configure
    if request.method == 'POST':
        try:
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
    global train_configure
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
def query_experiment():
    if request.method == 'POST':
        subject_id = request.form["subject_id"]
        experiment_id = db.session.query(RealTimeData.experiment_id) \
            .filter(RealTimeData.subject_id.in_([subject_id])) \
            .distinct() \
            .all()

        return jsonify(experiment_id=experiment_id)


# query the saved realtime data for a given training subject and experiment
@blueprint.route('/database/query/realtime_data', methods=['GET', 'POST'])
@login_required
def query_realtime_data():
    if request.method == 'POST':
        experiment_id = request.form["experiment_id"]
        subject_id = request.form["subject_id"]

        realtime_data = db.session.query(RealTimeData) \
            .filter(RealTimeData.experiment_id.in_([experiment_id])) \
            .filter(RealTimeData.subject_id.in_([subject_id])) \
            .all()

        time_stamp = []
        pull_force = []
        pull_velocity = []
        pull_distance = []
        completions = []
        for i in range(len(realtime_data)):
            time_stamp.append(realtime_data[i].time_stamp)
            pull_force.append(realtime_data[i].pull_force)
            pull_velocity.append(realtime_data[i].pull_velocity)
            pull_distance.append(realtime_data[i].pull_distance)
            completions.append(realtime_data[i].completions)

        return jsonify(time_stamp=time_stamp,
                       pull_force=pull_force,
                       pull_velocity=pull_velocity,
                       pull_distance=pull_distance,
                       completions=completions)


# delete the record for a given experiment id and subject id
@blueprint.route('/database/delete/record', methods=['GET', 'POST'])
@login_required
def delete_record():
    if request.method == 'POST':
        experiment_id_del = request.form["experiment_id"]
        subject_id_del = request.form["subject_id"]

        RealTimeData.query.filter_by(experiment_id=experiment_id_del, subject_id=subject_id_del).delete()
        db.session.commit()

        return jsonify(msg="The record is deleted, please refresh the page.")


@blueprint.route('/index/update/metadata', methods=["GET", "POST"])
def update_metadata():
    global manager
    if request.method == 'POST':
        return jsonify(remain_time=manager.remain_time,
                       force_val=manager.metadata.pull_force,
                       velocity_val=manager.metadata.pull_velocity,
                       distance_val=manager.metadata.pull_distance,
                       completions_val=manager.metadata.completions)


@blueprint.route('/index/interrupt', methods=["GET", "POST"])
def interrupt():
    global manager
    if request.method == 'POST':
        manager.interrupt = True
        return jsonify(msg="Process Interrupted")


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
