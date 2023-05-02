# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 02:00:50 2023

@author: mathi
"""
from helper import accurate_delay


class Motor():
    def __init__(self,dirPin,stepPin):
        self.direction = None
        self.dirPin = dirPin
        self.stepPin = stepPin
        self.position = 0
        self.history = [0]
        self.brother = None
        self.limit = None
    
    def run(self,steps=1,speed = 1):
        steps = int(abs(steps))
        if self.direction == "L" or self.direction == "D":
            update = -1
        else:
            update = 1
            
        if steps != 0:
            for x in range(steps):
                #Single pulse
                self.position = self.position + update
                self.history.append(self.position)
                self.brother.history.append(self.brother.position)
                
                self.stepPin.write(1)
                accurate_delay(speed)
                self.stepPin.write(0)
                accurate_delay(speed)
    
    def setBrother(self,bro):
        self.brother = bro
    
    def setLimit(self,limit):
        self.limit = limit
    
    def switchDirection(self):
        if self.direction == "R":
            Motor.setLeft()
        elif self.direction == "L":
            Motor.setRight()
        elif self.direction == "D":
            Motor.setUp()
        else:
            Motor.setDown()

