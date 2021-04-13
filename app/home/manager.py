# database connection
import random
import time
import timeit
#import threading
from multiprocessing import Process, Value

from app import db
from app.base.models import Configure, Experiment, Subject, RealTimeData
from .hardware_manager import hardwareManager
from datetime import datetime
from .hx711 import HX711



class Manager:
    def __init__(self):
        # initialize attributes here
        # global variables
        self.remain_time = 0
        self.interrupt = False

        self.metadata = RealTimeData()
        self.reset_metadata()
        self.hardwareManager = hardwareManager()

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
        self.reset_metadata()
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
    
        
        #self.hardwareManager.task(train_configure.required_distance, train_configure.required_force)
        
        #thread1 = threading.Thread(target = self.hardwareManager.task, args = (train_configure.required_distance, train_configure.required_force))
        completions = Value('i', 0)
        speed = Value('d', 0)
        flag = Value('i', True)
        p = Process(target = self.hardwareManager.task, args = (speed, completions, flag, train_configure.required_distance, train_configure.required_force))
        #thread1.start()
        print("task start!!!!!!")
        p.start()
        start = timeit.default_timer()
        end = timeit.default_timer()
        self.remain_time = exp_info.duration - (end - start)
        #while (self.remain_time > 0) and (not self.interrupt):
        while p.is_alive():
            self.metadata.time_stamp = datetime.now()
            #print("checkpoint")
            # TODO: change the following data retrieving approaches
            # TODO: also integrate the food dispenser
            self.metadata.pull_force = self.hardwareManager.get_average_weight()
            self.metadata.pull_velocity = speed.value
            self.metadata.pull_distance = self.hardwareManager.distance.value
            self.metadata.completions = completions.value

            # write the metadata into our database
            db.session.merge(self.metadata)
            db.session.commit()

            # TODO: you may want to change the sampling rate
            time.sleep(0.2)
            end = timeit.default_timer()
            self.remain_time = exp_info.duration - (end - start)
            
            if self.remain_time <= 0 or self.interrupt:
                flag.value = False
                break
        
        p.join()
        self.remain_time = 0
        self.metadata.pull_force = 0
        self.metadata.pull_velocity = speed.value
        self.metadata.pull_distance = self.hardwareManager.distance.value
        self.metadata.completions = completions.value
        db.session.merge(self.metadata)
        db.session.commit()
