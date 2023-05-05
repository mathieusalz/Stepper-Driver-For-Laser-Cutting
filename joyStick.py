# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 02:02:57 2023

@author: mathi
"""

from scipy.interpolate import interp1d
from pyfirmata import util


class JoyStick():
    '''
    Initializes the joystick
    Inputs:
        - Arduino board
        - Motor System
    '''
    def __init__(self,board,MotorSystem):
        it = util.Iterator(board)
        it.start()
        
        # the speed of the motors is determined by the analog input from the joystick
        # Analog inputs connected to Analog Pins 0 and 1 on Arduino
        vrx = board.get_pin("a:0:i")
        vry = board.get_pin("a:1:i")
        
        # Allows analog pin to communicate with computer
        vrx.enable_reporting()
        vry.enable_reporting()
        
        self.vrx = vrx
        self.vry = vry
        self.MotorSystem = MotorSystem
        
        # The mapper takes the output of the joystick which will be between
        # 0 and 0.4 and interpolates between the range 0.1 and 0.01 which
        # represents the speed of the stepper motors (the values correspond
        # to the pwm width - the smaller the width, the faster the steps)
        self.mapper = interp1d([0,0.4],[0.1,0.01])


    def control(self): 
        self.vrx.enable_reporting()
        self.vry.enable_reporting()
        
        # Read the joystick outputs for x and y
        x_read = self.vrx.read()
        y_read = self.vry.read()
    
    
        # Want to make sure that both are not None or else it will crash
        if x_read is not None and y_read is not None:
            
            x_speed, x_run, x_dir = self.speedMapper(x_read)
            y_speed, y_run, y_dir = self.speedMapper(y_read)
            
            if x_dir:
                self.MotorSystem.setRight()
            else: 
                self.MotorSystem.setLeft()
            
            if y_dir:
                self.MotorSystem.setDown()
            else:
                self.MotorSystem.setUp()
            
            if (x_run):
                self.MotorSystem.X_Motor.run(steps= 1,speed = float(x_speed))
                
            if (y_run):
                self.MotorSystem.Y_Motor.run(steps = 1, speed = float(y_speed))
    
    # Takes a joystick output and converts it into a stepper motor speed
    # If joystick reading is between 0.4 and 0.6 the motor does not run
    def speedMapper(self,reading):
        direction = None
        if (reading < 0.6 and reading > 0.4):
            motor_speed = 0
            run = False
        else:
            if reading > 0.6:
                direction = True
                vel = reading - 0.6
            else:
                direction = False
                vel = 0.4 - reading
            motor_speed = self.mapper(vel)
            
            run = True
        
        return motor_speed,run,direction
    