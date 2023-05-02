# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 02:02:57 2023

@author: mathi
"""

from scipy.interpolate import interp1d
from pyfirmata import Arduino, util


class JoyStick():
    def __init__(self,board,MotorSystem):
        it = util.Iterator(board)
        it.start()
        
        vrx = board.get_pin("a:0:i")
        vry = board.get_pin("a:1:i")
        
        vrx.enable_reporting()
        vry.enable_reporting()
        
        self.vrx = vrx
        self.vry = vry
        self.MotorSystem = MotorSystem
        self.mapper = interp1d([0,0.4],[0.1,0.01])


    def control(self): 
        self.vrx.enable_reporting()
        self.vry.enable_reporting()
        
        x_read = self.vrx.read()
        y_read = self.vry.read()
    
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
    
    def setMapper(self,lower_lim, upper_lim):
        self.mapper = interp1d([0,0.45],[lower_lim,upper_lim])