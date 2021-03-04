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
    exp_configure = db.session.query(Configure).get(0)
    return render_template('ui-configure.html',
                           input_force=exp_configure.required_force,
                           input_distance=exp_configure.required_distance,
                           input_time_window=exp_configure.allowable_time_window)

@blueprint.route('/configure/upload', methods=['GET', 'POST'])
@login_required
def configure_upload():
    if request.method == 'POST':
        exp_configure = Configure()
        exp_configure.id = int(request.form["experiment_setting_id"])
        exp_configure.required_force = request.form["input_force"]
        exp_configure.required_distance = request.form["input_distance"]
        exp_configure.allowable_time_window = request.form["input_time_window"]

        db.session.merge(exp_configure)
        db.session.commit()

        return jsonify(msg="Experiment Setting Uploaded")


@blueprint.route('/configure/query', methods=['GET', 'POST'])
@login_required
def configure_query():
    if request.method == 'POST':
        configure_id = int(request.form["experiment_setting_id"])
        exp_configure = db.session.query(Configure).get(configure_id)
        if exp_configure is None:
            exp_configure = Configure()
            exp_configure.id = configure_id

            db.session.merge(exp_configure)
            db.session.commit()

        return jsonify(input_force=exp_configure.required_force,
                       input_distance=exp_configure.required_distance,
                       input_time_window=exp_configure.allowable_time_window)


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

        if not template.endswith( '.html' ):
            template += '.html'

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( template, segment=segment )

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except:
        return render_template('page-500.html'), 500


# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None  
