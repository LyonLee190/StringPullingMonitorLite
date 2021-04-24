# Need to install advpistepper (have to be install by python setup.py) & hx711 (pip)
import subprocess
import logging
import pigpio
from hx711 import HX711
import sys
from Motor import ULN2003

import busio
import digitalio
import board
import math
import threading
from multiprocessing import Process, Value
import adafruit_mcp3xxx.mcp3008 as MCP
import time
import RPi.GPIO as GPIO

# import the library
from RpiMotorLib import RpiMotorLib
from adafruit_mcp3xxx.analog_in import AnalogIn

ADC_Sample_Interval = 0.0000005
AVG_Step = 500
referenceUnit = 100


class hardwareManager:
    
    #gpio1: for dispenser's motor
    #gpio2: for pulley wheel's motor
    def __init__(self, gpio1 = [18, 23, 24, 25], gpioLoad = [27, 17]):
        self.spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        self.cs = digitalio.DigitalInOut(board.D5)
        self.mcp = MCP.MCP3008(self.spi, self.cs)
        self.channel = AnalogIn(self.mcp, MCP.P0)
        #specify the motor type, the library may need to be changed if the motor is replaced 
        self.mymotortest = RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ")
        self.gpio1 = gpio1
        #use pin27 and 17 to connect the driver board
        self.hx = HX711(27, 17)
        
        self.hx.reset()
        self.hx.zero()
        
        self.speed = 0
        self.completions = 0
        self.flag = False
        print("Tare done! Add weight now...")
        
        self.distance = Value('i', 0)
        self.cmd = Value('i', 0)
    
    def cleanAndExit(self):
        #clean up the GPIOs
        print("Cleaning...")

        GPIO.cleanup()
        
        print("Bye!")
        sys.exit()
#      
#      
    def speedLevel(self, val, required_force, deviation = 0.05):
        #if the pull force on the string exceeds the bound, the motor will increase the speed otherwise decrease
        #the speed increase or decrease by 50 and the maximum speed is 1400
        #deviation is the allowable range, speed is not changed if ratio is in [1-deviation, 1+deviation]
        ratio = self.get_average_weight() / required_force
        if abs(1 - ratio) <= deviation:
            if self.speed == 0:
                self.speed = 50
        elif ratio < 1:
            if self.speed < 50:
                self.speed = 0
            else:
                self.speed -= 50
            
        if ratio > 1:
            if self.speed < 1350:
                self.speed = self.speed + 50
            else:
                self.speed = 1400

            
    def get_average_weight(self, mean = 30):
        #this function is to convert the readings of the loadcell to grams
        #the readinds are also influenced by temperature
        #parameter "mean" is how many times the weight is sampled
        val = abs(self.hx.get_weight_mean(mean))
        if (val < 700):
            return 0
        else:
            val = round((val - 450)/2250, 1)
            return val
        
    def run(self,degree, direction = True):
        #turn the degree to steps 
        self.degree = math.floor(degree*512/360)
        self.mymotortest.motor_run(self.gpio1, .005, self.degree, direction, False, "full", .05)
        time.sleep(2)
    
    def raw_dispense(self):
        #dispense food pallets and check if food pallets are dropped
        t1 = threading.Thread(target = self.run, args = (30,))
        t1.start()
        while True:
            val = self.channel.value
            if (val < 60000):
                t1.join()
                return True
            time.sleep(ADC_Sample_Interval)
            if t1.is_alive() == False:
                return False
            
    def dispense(self, number = 1, maximum_wait_time = 25):
        #set how many food pallets shall be dropped and the maximum wait time
        #if the food is not dropped within the wait time it reports an error
        count = number
        time1 = time.time()
        while( count > 0):
            if time.time() - time1 >= maximum_wait_time:
                print("Error")
                return False
            
            if self.raw_dispense():
                count -= 1
                print("one pallet dropped")
            time.sleep(0.1)
        return True
        
    def stop_motor(self):
        self.cmd.value = 0

    def run_motor(self):
        self.cmd.value = 1
        
    def close_motor(self):
        self.cmd.value = -1

    def task(self, s, c, f, rotations = 1, force = 50):
        steps = round(rotations * 512)
        c.value = self.completions
        self.cmd.value = 0
        speed = Value('d', 0)
        self.distance.value = 0
        self.stepper = ULN2003([12, 16, 20, 21])
        p = Process(target = self.stepper.execute, args=(self.cmd, speed, self.distance))
        p.start()
        while f.value:
                val = self.get_average_weight(30)
                
                #print(self.stepper.current_speed)
                print(val)
                self.speedLevel(val, force)
                if (self.speed == 0):
                    # speed equals to 0, stop the motor
                    self.stop_motor()
                    s.value = self.speed

                else:
                    # speed not equals to 0, run the motor with speed
                    self.run_motor()
                    speed.value = self.speed
                    s.value = self.speed
                time.sleep(0.25)
                
                if self.distance.value >= steps:
                    break
                


        # job finished, close and zero the stepper
        self.close_motor()
        self.speed = 0
        s.value = self.speed
        p.join()
        p.terminate()
        self.stepper.zero()
        
        if f.value:
            self.completions += 1
            self.dispense()
            c.value = self.completions
        return steps
            
if __name__ == "__main__":
    thread1 = hardwareManager()
    thread1.task(rotations = 1)
    thread1.cleanAndExit()
    
    