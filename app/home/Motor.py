import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
from multiprocessing import Value
import math

#Speed Limit (half step) 1/ 1400

class ULN2003:
    def __init__(self, GPIO = [12, 16, 20, 21]):
        self.mymotortest = RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ")
        self.GPIO = GPIO
        self._distance = 0
        self._speed = 500
        self._acceleration = 10
        self._deceleration = 10
        
    def set_acceleration(self, acceleration):
        self._acceleration = acceleration
        
    def set_deceleration(self, deceleration):
        self._deceleration = deceleration
        
    def set_speed(self, speed):
        self._speed = speed
    
#      def accelerate(self, target_speed):
#          while(self._speed < target_speed):
            

    def zero(self):
        self._distance = 0
        
    def current_distance(self):
        return self._distance
        
    def run(self, step = 1, direction = True):
        self.mymotortest.motor_run(self.GPIO, 1/self._speed, step, direction, False, "half", 0)
        self._distance += 1
        
    #def accelerate(self, 
        
    def stop(self):
        pass

    '''
    cmd: Variable representing the motor's state
    cmd has to be a multiprocess.Value Object
    -1: exit
    0: stop
    1: run
    2: accerelate
    3: decerelate
    '''
    def execute(self, cmd, speed, distance):
        while cmd.value != -1:
            if cmd.value == 0:
                self.stop()
                distance.value = self.current_distance()
            elif cmd.value == 1:
                self.set_speed(speed.value)
                self.run()
                distance.value = self.current_distance()
            elif cmd.value == 2:
                self.set_speed(speed.value)
                self.run()
                distance.value = self.current_distance()
            elif cmd.value == 3:
                self.set_speed(speed.value)
                self.run()
                distance.value = self.current_distance()
    

if __name__ == "__main__":
    motor = ULN2003()
    motor.run()
