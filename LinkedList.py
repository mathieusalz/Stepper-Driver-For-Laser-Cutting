# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 15:57:11 2023

@author: mathi
"""

from Element import Element

class LinkedList():
    def __init__(self):
        self.start = None
        self.centerRight = None
        self.centerLeft = None
        self.centerUp = None
        self.centerDown = None
        self.leftTopCorner = None
        self.rightTopCorner = None
        self.rightBottomCorner = None
        self.leftBottomCorner = None
    
    def addElement(self,coord):
        element = Element(coord)
        return element

    def fillList(self,x_coords,y_coords,x_steps,y_steps,shape):
        start_point = self.addElement((x_coords[0],y_coords[0]))
        self.start = start_point
        
        if shape == "Rectangle":
            self.leftTopCorner = start_point
        elif shape == "Circle":
            self.centerLeft = start_point
        
        last_point = start_point       
                     
        for i in range(1,len(x_coords)):
            point = self.addElement((x_coords[i],y_coords[i]))
            last_point.next = point
            
            if shape == "Rectangle":
                if i == 2*x_steps:
                    self.rightTopCorner = point
                if i == 2*x_steps + 2*y_steps:
                    self.rightBottomCorner = point
                if i == 4*x_steps + 2*y_steps:
                    self.leftBottomCorner = point
                    
            elif shape == "Circle":
                if i> 0 and i % x_steps == 0:
                    if i /x_steps == 1:
                        self.centerTop = point
                    elif i/x_steps == 2:
                        self.centerRight = point
                    else:
                        self.centerDown = point
                        
            last_point = point

        last_point.next = start_point