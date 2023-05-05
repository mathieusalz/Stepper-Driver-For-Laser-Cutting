# -*- coding: utf-8 -*-
"""
Created on Wed May  3 18:10:10 2023

@author: mathi
"""


from window_test import calibration_and_center, shape_Choice, cut_shape


cut_wizard = calibration_and_center()

while cut_wizard:
    
    path = shape_Choice()
            
    if path is not None:
        cut_wizard = cut_shape(path)
        
    else:
        break
