# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 00:39:12 2023

@author: mathi
"""
from helper import x_to_steps, y_to_steps
from LinkedList import LinkedList
import math
import numpy as np
import matplotlib.pyplot as plt

def circle(x_pos, y_pos, radius):
    
    circlePath = LinkedList()
    
    x_steps, _ = x_to_steps(radius)
    y_steps, _ = y_to_steps(radius)    
    
    x_coords = np.linspace(x_pos-x_steps, x_pos + x_steps, 2*x_steps)
    x_points = np.linspace(-radius, radius, 2*x_steps)
    
    y_coords = []    
    
    last_point = None
    next_flipped = None

    #Find each real y_point for each feasible x_point
    for i,x_point in enumerate(x_points):
        y_point = math.sqrt((radius**2-(x_point)**2))
        y_step, _ = y_to_steps(y_point)
        y_coords.append(y_step+y_pos)
        
        point = circlePath.addElement((x_coords[i],y_coords[i]))
        y_flipped_point = circlePath.addElement((x_coords[i],2*y_pos - y_coords[i]))
        
        
        if i == 0:
            circlePath.start = point
            circlePath.centerLeft = point
            next_flipped = circlePath.start
        else:
            last_point.next = point
            y_flipped_point.next = next_flipped
            last_point = point
            next_flipped = y_flipped_point
        
        last_point = point
    
        if i/x_steps == 1: 
            circlePath.centerTop = point
            circlePath.centerDown = y_flipped_point
    
    point.next = y_flipped_point.next
        
    circlePath.centerRight = point
    
    return (x_steps, y_steps, circlePath)

def truncateCircle(x_steps, y_steps, circlePath, truncate_side):
    
    if truncate_side == "Left":
        circlePath.start = circlePath.centerDown
        steps_to_go = int(x_steps*0.707//1) 
    elif truncate_side == "Right":
        circlePath.start = circlePath.centerTop
        steps_to_go = int(x_steps*0.707//1) 
    elif truncate_side == "Top":
        circlePath.start = circlePath.centerLeft
        steps_to_go = int(x_steps-x_steps*0.707//1) 
    else:
        circlePath.start = circlePath.centerRight
        steps_to_go = int(x_steps-x_steps*0.707//1) 
    
    current = circlePath.start
    
    for i in range(steps_to_go):
        current = current.next
        
    walker = current.next
    for i in range(2*(x_steps-steps_to_go)):
        walker = walker.next
    
    current.next = walker
    
def rectangle(x_pos, y_pos, x_length, y_length):
    x_steps, x_length = x_to_steps(x_length/2)
    y_steps, y_length = y_to_steps(y_length/2)
    
    rectanglePath = LinkedList()
    
    rectanglePath.leftTopCorner = rectanglePath.addElement((x_pos - x_steps, y_pos + y_steps))
    rectanglePath.rightTopCorner = rectanglePath.leftTopCorner.setNext((x_pos + x_steps, y_pos + y_steps))
    rectanglePath.leftBottomCorner = rectanglePath.rightTopCorner.setNext((x_pos + x_steps, y_pos - y_steps))
    rectanglePath.leftBottomCorner = rectanglePath.rightBottomCorner.setNext((x_pos-x_steps, y_pos-y_steps))
    rectanglePath.leftBottomCorner.next = rectanglePath.leftTopCorner
    
    return (x_steps, y_steps, rectanglePath)
        
def truncateRectangle(x_steps,y_steps,rectanglePath, truncate_side):
    
    if truncate_side == "Top Right":
        trunc_1 = rectanglePath.leftTopCorner.setNext((rectanglePath.leftTopCorner.coord[0]+x_steps//(3/4),rectanglePath.leftTopCorner.coord[1]))
        trunc_2 = trunc_1.setNext((trunc_1.coord[0],trunc_1.coord[1]-y_steps//4))
        trunc_3 = trunc_2.setNext((rectanglePath.rightTopCorner.coord[0],trunc_2.coord[1]))
        trunc_3.next = rectanglePath.rightBottomCorner
        
    elif truncate_side == "Bottom Right":
        trunc_1 = rectanglePath.rightTopCorner.setNext((rectanglePath.rightTopCorner.coord[0], rectanglePath.rightTopCorner.coord[1]-y_steps//(3/4)))
        trunc_2 = trunc_1.setNext((trunc_1.coord[0]-x_steps//4,trunc_1.coord[1]))
        trunc_3 = trunc_2.setNext((trunc_2.coord[0],rectanglePath.rightBottomCorner.coord[1]))
        trunc_3.next = rectanglePath.leftBottomCorner
        
    elif truncate_side == "Bottom Left":
        trunc_1 = rectanglePath.rightBottomCorner.setNext((rectanglePath.rightBottomCorner.coord[0]-x_steps//(3/4),rectanglePath.rightBottomCorner.coord[1]))
        trunc_2 = trunc_1.setNext((trunc_1.coord[0],trunc_1.coord[1]+y_steps//4))
        trunc_3 = trunc_2.setNext((rectanglePath.leftBottomCorner.coord[0],trunc_2.coord[1]))
        trunc_3.next = rectanglePath.leftTopCorner
        
    else:
        rectanglePath.start = rectanglePath.leftBottomCorner
        trunc_1 = rectanglePath.leftBottomCorner.setNext((rectanglePath.leftBottomCorner.coord[0],rectanglePath.leftBottomCorner.coord[1]+y_steps//(3/4)))
        trunc_2 = trunc_1.setNext((trunc_1.coord[0]+x_steps//4,trunc_1.coord[1]))
        trunc_3 = trunc_2.setNext((trunc_2.coord[0],rectanglePath.leftTopCorner.coord[1]))
        trunc_3.next = rectanglePath.rightTopCorner
