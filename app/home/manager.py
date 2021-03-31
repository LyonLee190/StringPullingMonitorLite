# database connection
import random
import time
import timeit

from app import db
from app.base.models import Configure, Experiment, Subject, RealTimeData

from datetime import datetime


class Manager:
    def __init__(self):
        # initialize attributes here
        # global variables
        self.remain_time = 0
        self.interrupt = False

        self.metadata = RealTimeData()
        self.reset_metadata()

    def reset_metadata(self):
        self.remain_time = 0
        self.interrupt = False

        self.metadata.experiment_id = "sample"
        self.metadata.subject_id = "sample"
        self.metadata.time_stamp = datetime.now()
        self.metadata.pull_force = 0
        self.metadata.pull_velocity = 0
        self.metadata.pull_distance = 0
        self.metadata.completions = 0

    def execute(self, exp_info, subject, train_configure):
        # experiment id:            exp_info.id
        # duration:                 exp_info.duration
        # subject id:               subject.id
        # required pull force:      train_configure.required_force
        # required pull distance:   train_configure.required_distance
        # allowable time window:    train_configure.allowable_time_window

        self.metadata.experiment_id = exp_info.id
        self.metadata.subject_id = subject.id
        # other attributes have to be updated during the training
        # current time stamp:       self.metadata.time_stamp
        # current pull force:       self.metadata.pull_force
        # current pull velocity:    self.metadata.pull_velocity
        # current pull distance:    self.metadata.pull_distance
        # number of completions:    self.metadata.completions

        start = timeit.default_timer()
        end = timeit.default_timer()
        self.remain_time = exp_info.duration - (end - start)
        while (self.remain_time > 0) and (not self.interrupt):
            self.metadata.time_stamp = datetime.now()
            # TODO: change the following data retrieving approaches
            # TODO: also integrate the food dispenser
            self.metadata.pull_force = random.randint(0, 64)
            self.metadata.pull_velocity = random.randint(0, 64)
            self.metadata.pull_distance = random.randint(0, 64)
            self.metadata.completions = random.randint(0, 64)

            # write the metadata into our database
            db.session.merge(self.metadata)
            db.session.commit()

            # TODO: you may want to change the sampling rate
            time.sleep(1)
            end = timeit.default_timer()
            self.remain_time = exp_info.duration - (end - start)
        self.reset_metadata()
