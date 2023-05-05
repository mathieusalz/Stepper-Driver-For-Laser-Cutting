# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 02:03:20 2023

@author: mathi
"""
import time
from datetime import datetime

# Definition of Ranges for each motor
x_range = 69 #mm
y_range = 49 #mm

# Definition of Sensitivity for each motor
x_sensitivity = 0.00167 # mm
y_sensitivity = 0.00267 # mm

'''
Function: Turns a length steps that a motor can accomplish given its sensitivity
Returns: 
    - number of steps
    - new length adjusted for the sensitivity of the motor
'''
def length_to_steps(length,sensitivity):
    length = length - length/sensitivity%1*sensitivity+sensitivity
    steps = (length/sensitivity)//1
    return int(steps), length

def steps_to_length(steps, sensitivity):
    return steps*sensitivity

def x_steps_to_length(steps):
    return steps_to_length(steps,x_sensitivity)

def y_steps_to_length(steps):
    return steps_to_length(steps,y_sensitivity)

# Turns a length into steps for the x motor
def x_to_steps(length):
    return length_to_steps(length,x_sensitivity)

# Turns a length into steps for the y motor
def y_to_steps(length):
    return length_to_steps(length,y_sensitivity)

# Provides delay in milliseconds
def accurate_delay(delay):
    _ = time.perf_counter() + delay/1000
    while time.perf_counter() < _:
        pass
    