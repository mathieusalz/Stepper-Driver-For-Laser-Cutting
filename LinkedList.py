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
        
        last_point = start_point       
                     
        for i in range(1,len(x_coords)):
            point = self.addElement((x_coords[i],y_coords[i]))
            last_point.next = point
            last_point = point

        last_point.next = start_point