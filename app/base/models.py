# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app import db, login_manager

from app.base.util import hash_pass

class Experiments(db.Model):
    experiment_id = Column(db.String, primary_key=True)

    date = Column(db.DateTime, nullable=False)
    required_force = Column(db.Float, nullable=False)
    required_distance = Column(db.Float, nullable=False)
    allowable_time_window = Column(db.Integer, nullable=False)
    duration = Column(db.Integer, nullable=False)
    comment = Column(db.String)

    realTimeData = relationship("RealTimeData", uselist=False, back_populates="experiments")

    def __repr__(self):
        return '<Experiments %r %r %r %r %r %r %r>' % (self.experiment_id,
                                                       self.date,
                                                       self.required_force,
                                                       self.required_distance,
                                                       self.allowable_time_window,
                                                       self.duration,
                                                       self.comment)


class Subjects(db.Model):
    subject_id = Column(db.String, primary_key=True)

    realTimeData = relationship("RealTimeData", uselist=False, back_populates="subjects")

    def __repr__(self):
        return '<Experiments %r>' % self.subject_id


class RealTimeData(db.Model):
    experiment_id = Column(db.String, ForeignKey('experiments.experiment_id'), primary_key=True)
    subject_id = Column(db.String, ForeignKey('subjects.subject_id'), primary_key=True)
    time_stamp = Column(db.DateTime, primary_key=True)

    pull_force = Column(db.Float, nullable=False)
    pull_velocity = Column(db.Float, nullable=False)
    pull_distance = Column(db.Float, nullable=False)
    completions = Column(db.Integer, nullable=False)

    experiments = relationship("Experiments", back_populates="realTimeData")
    subjects = relationship("Subjects", back_populates="realTimeData")

    def __repr__(self):
        return '<Experiments %r %r %r %r %r %r %r>' % (self.experiment_id,
                                                       self.subject_id,
                                                       self.time_stamp,
                                                       self.pull_force,
                                                       self.pull_velocity,
                                                       self.pull_distance,
                                                       self.completions)

class User(db.Model, UserMixin):

    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(Binary)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass( value ) # we need bytes here (not plain str)
                
            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None
