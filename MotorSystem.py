# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 23:50:40 2023

@author: mathi
"""

from Motor import Motor
from helper import x_range, y_range, x_to_steps, y_to_steps
import numpy as np

class Motor_System():
    def __init__(self,board):
        dirX = board.digital[3]
        stepX = board.digital[4]
        
        dirY = board.digital[6]
        stepY = board.digital[5]
        self.X_Motor = Motor(dirX,stepX)
        self.Y_Motor = Motor(dirY,stepY)
        self.relativeCenter = None
        self.setBrothers()
        self.setLimits()
    
    def setRelativeCenter(self,coords):
        self.relativeCenter = coords
    
    def setPosition(self,coords):
        self.X_Motor.position = coords[0]
        self.Y_Motor.position = coords[1]
    
    def setBrothers(self):
        self.X_Motor.setBrother(self.Y_Motor)
        self.Y_Motor.setBrother(self.X_Motor)
    
    def setLeft(self):
        self.X_Motor.dirPin.write(1)
        self.X_Motor.direction = "L"

    def setRight(self):
        self.X_Motor.dirPin.write(0)
        self.X_Motor.direction = "R"
        
    def setDown(self):
        self.Y_Motor.dirPin.write(0)
        self.Y_Motor.direction = "D"

    def setUp(self):
        self.Y_Motor.dirPin.write(1)
        self.Y_Motor.direction = "U"
    
    def getPosition(self):
        return self.X_Motor.position,self.Y_Motor.position
    
    def setLimits(self):
        x_upper = x_to_steps(x_range)[0] - 10
        y_upper = y_to_steps(y_range)[0] - 10
        self.X_Motor.setLimit(x_upper)
        self.Y_Motor.setLimit(y_upper)
        
    def goUp(self,steps):
        self.setUp()
        self.Y_Motor.run(steps,0.1)

    def goDown(self,steps):
        self.setDown()
        self.Y_Motor.run(steps,0.1)

    def goLeft(self,steps):
        self.setLeft()
        self.X_Motor.run(steps,0.1)

    def goRight(self,steps):
        self.setRight()
        self.X_Motor.run(steps,0.1)
    
    def center(self):
        x_steps_to_half,_ = x_to_steps(y_range/2)
        y_steps_to_half,_ = y_to_steps(x_range/2)
        self.goUp(y_steps_to_half)
        self.goLeft(x_steps_to_half)
        
    def moveTo(self,x,y,speed=0.5):
 
        
        x_dist = x - self.X_Motor.position 

        y_dist = y - self.Y_Motor.position
        
        
        if isinstance(y_dist,(float,int,np.integer)):
            if y_dist < 0:
                self.setDown()
            else:
                self.setUp()
                
            if x_dist <0:
                self.setLeft()
            else:
                self.setRight()
            
            if x_dist == 0:
                self.Y_Motor.run(y_dist,speed)
            
            elif y_dist == 0:
                self.X_Motor.run(x_dist,speed)
            
            else:
                self.Y_Motor.run(y_dist,speed)
                self.X_Motor.run(x_dist,speed)
       
        else:
        
            if y_dist[0] < 0:
                self.setDown()
            else:
                self.setUp()
                
            if x_dist <0:
                self.setLeft()
            else:
                self.setRight()
            
            if x_dist == 0:
                self.Y_Motor.run(y_dist[0],speed)
            
            elif y_dist[0] == 0:
                self.X_Motor.run(x_dist,speed)
            
            else:
                self.Y_Motor.run(y_dist[0],speed)
                self.X_Motor.run(x_dist,speed)
            