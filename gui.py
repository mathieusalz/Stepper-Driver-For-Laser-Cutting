'''
########################################################################
                                IMPORTS
########################################################################
'''

import PySimpleGUI as sg
from tkinter import *
from PIL import Image, ImageTk
import pyfirmata
from MotorSystem import Motor_System
from joyStick import JoyStick
import Shapes
from LinkedList import LinkedList
import matplotlib.pyplot as plt
from helper import x_to_steps, y_to_steps
import numpy as np
import time
from window import calibration_and_center, shape_Choice, cut_shape


'''
########################################################################
                            INITIALIZATIONS
########################################################################
'''

#board = pyfirmata.Arduino('COM9')
#MotorSys = Motor_System(board)
#joyStick = JoyStick(board,MotorSys)


'''
########################################################################
                                WORKFLOW
########################################################################
'''


cut_wizard = calibration_and_center( 
                                    #joyStick = joyStick, 
                                    #MotorSys = MotorSys, 
                                    #board = board,
                                    #known_position= False
                                    )
while cut_wizard:
    
    path = shape_Choice( 
                 #board = board,
                 #MotorSys = MotorSys
                 )

            
    if path is not None:
        
        cut_wizard = cut_shape(path
            #MotorSys, 
            #path,
            #board
            )
    else:
        break

'''
########################################################################
                                    PROGRAM END
########################################################################
'''        
        
board.sp.close()