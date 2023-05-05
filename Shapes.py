# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 00:39:12 2023

@author: mathi
"""
from helper import x_to_steps, y_to_steps
from LinkedList import LinkedList
import math
import numpy as np

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
        
        
            
        if i /x_steps == 1:
                circlePath.centerTop = point
                circlePath.centerBottom = y_flipped_point
    
    point.next = y_flipped_point.next
        
    circlePath.centerRight = point
    
    return (x_steps, y_steps, circlePath)

def truncateCircle(x_steps, y_steps, circlePath, truncate_side):
    
    truncatedCircle = LinkedList()
        
    if truncate_side == "Left":
        truncatedCircle.start = circlePath.centerDown
        compare_coord = 0
    elif truncate_side == "Right":
        truncatedCircle.start = circlePath.centerTop
        compare_coord = 0
    elif truncate_side == "Top":
        truncatedCircle.start = circlePath.centerLeft
        compare_coord = 1
    else:
        truncatedCircle.start = circlePath.centerRight
        compare_coord = 1
    
    steps_to_go = int(x_steps*0.707//1) 
    
    current = truncatedCircle.start
    
    for i in range(steps_to_go):
        current = current.next
        
    compare = current
    walker = current.next.next.next
    
    while True:
        if compare.coord[compare_coord] == walker.coord[compare_coord]:
            break
        else:
            walker = walker.next
    
    compare.next = walker
    
    return truncatedCircle


def rectangle(x_pos, y_pos, x_length, y_length):
    x_steps, x_length = x_to_steps(x_length/2)
    y_steps, y_length = y_to_steps(y_length/2)
    
    x_coords = np.linspace(x_pos-x_steps,x_pos+x_steps,2*x_steps)
    y_coords = np.linspace(y_pos+y_steps,y_pos-y_steps,2*y_steps)
    
    y_coords = np.append(np.ones(2*x_steps)*y_coords[0],y_coords)
    
    x_coords = np.append(x_coords,np.ones(2*y_steps)*x_coords[-1])
    
    x_coords = np.append(x_coords,np.linspace(x_pos+x_steps,x_pos-x_steps,2*x_steps))    
    y_coords = np.append(y_coords, np.ones(2*x_steps)*y_coords[-1])
    
    y_coords = np.append(y_coords,np.linspace(y_pos-y_steps,y_pos+y_steps,2*y_steps))
    x_coords = np.append(x_coords,np.ones(2*y_steps)*x_coords[-1])
    
    rectanglePath = LinkedList()
    
    rectanglePath.fillList(x_coords,y_coords,x_steps,y_steps, shape="Rectangle")

    
    return (x_steps, y_steps, rectanglePath)
        
def truncateRectangle(x_steps,y_steps,rectanglePath, truncate_side):
    
    truncatedRectangle = LinkedList()
    
    if truncate_side == "Top Right" or truncate_side == "Bottom Left":
        
        truncatedRectangle.start = rectanglePath.leftTopCorner if truncate_side == "Top Right" else rectanglePath.rightBottomCorner
        steps_to_go = int(x_steps*1.75)
        
    else:
        truncatedRectangle.start = rectanglePath.rightTopCorner if truncate_side == "Bottom Right" else rectanglePath.leftBottomCorner
        
        steps_to_go = int(y_steps*1.75)
        
    point = truncatedRectangle.start
    
    for i in range(steps_to_go):
        point = point.next
    
    walker = point.next
    
    steps_to_go = int(x_steps*0.25 + y_steps*0.25)
    for i in range(steps_to_go):
        walker = walker.next
    
    point.next = walker
    
    point = truncatedRectangle.start
    