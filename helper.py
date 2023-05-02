# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 02:03:20 2023

@author: mathi
"""
import time
import numpy as np
import math
import matplotlib.pyplot as plt

x_range = 69 #mm
y_range = 49 #mm
#x_sensitivity = 0.00157          # millimeters x motor moves in 1 full step
#y_sensitivity = 0.0028          # millimeters y motor moves in 1 full step
x_sensitivity = 0.00267
y_sensitivity = 0.00167 

#Turns a length into a unit amount of steps
def length_to_steps(length,sensitivity):
    length = length - length/sensitivity%1*sensitivity+sensitivity
    steps = (length/sensitivity)//1
    return int(steps), length

def x_to_steps(length):
    return length_to_steps(length,x_sensitivity)

def y_to_steps(length):
    return length_to_steps(length,y_sensitivity)


def accurate_delay(delay):
    ''' Function to provide accurate time delay in millisecond
    '''
    _ = time.perf_counter() + delay/1000
    while time.perf_counter() < _:
        pass