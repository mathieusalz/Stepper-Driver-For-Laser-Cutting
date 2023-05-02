# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 18:04:42 2023

@author: mathi
"""
import PySimpleGUI as sg
import Shapes
import numpy as np
from helper import x_to_steps, y_to_steps
from tkinter import *
from copy import deepcopy
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


lay_circle = [[sg.Text('Circle')],
            [sg.Text('Enter Circle radius'), sg.InputText(key="radius_input")],
            [sg.Checkbox("Truncated",key="Truncated Circle",enable_events=True)],
            [sg.Radio('Top','sides', key ='U',visible= False,enable_events=True), 
             sg.Radio('Left','sides', key='L',visible= False,enable_events=True),
             sg.Radio('Bottom','sides', key ='D',visible= False,enable_events=True),
             sg.Radio('Right','sides', key ='R',visible= False,enable_events=True)
             ]]

lay_rectangle = [[sg.Text('Rectangle')],
            [sg.Text('Enter X length'), sg.InputText(key="x length")],
            [sg.Text('Enter Y length'), sg.InputText(key='y length')],
            [sg.Checkbox("Truncated",key="Truncated Rectangle",enable_events=True)],
            [sg.Radio('Top Right','corners', key ='TR',visible= False,enable_events=True), 
             sg.Radio('Top Left','corners', key='TL',visible= False,enable_events=True),
             sg.Radio('Bottom Right','corners', key ='BR',visible= False,enable_events=True),
             sg.Radio('Bottom Left','corners', key ='BL',visible= False,enable_events=True)
             ]]

#                               Drawing Choice Layout
lay_draw = [[sg.Text('Drawing Parameters')],
            [sg.Text('Enter X length'), sg.InputText(key="x draw length")],
            [sg.Text('Enter Y length'), sg.InputText(key='y draw length')],
            [sg.Button("Start Drawing")]
            ]

#                               Shape Configuration Layout
lay_shapeChoice = [[sg.Text('Choose a shape:')],
          [sg.Radio('Circle','shapes', key ='Circle', enable_events=True), 
           sg.Radio('Rectangle','shapes', key='Rectangle', enable_events=True),
           sg.Radio('Draw', 'shapes', key='Draw', enable_events=True)],
          [sg.Column(lay_circle, key='CircleConfiguration', visible= False), 
           sg.Column(lay_rectangle, visible=False, key='RectangleConfiguration'),
           sg.Column(lay_draw, visible=False, key='DrawConfiguration')],
          [sg.Button('OK'),sg.Button('Cancel')]]

#                               Joystick Layout
lay_joystick= [[sg.Text('Calibrate and Center:')],
               [sg.Text('Current position: unknown',key="Position")],
          [sg.Button('Calibrate'),
           sg.Button('Center'),
           sg.Button('Set Center'),
           sg.Button("Cancel")]]

#                               Cutting Layout
lay_cut = [[sg.Text('Ready to Cut:')],
          [sg.Button('Go to Start'),
           sg.Button('Begin'),
           sg.Button("Stop Cutting"),
           sg.Button("New Shape"),
           sg.Button("Cancel")],
          [sg.Slider(range=(0.1,1), default_value=1, resolution = 0.01, 
                     orientation='horizontal',enable_events=True,key="speed")]]


circle_trunc_radios = ["U","L","D","R"]
rectangle_trunc_radios = ["TL","TR","BR","BL"]

#Updates the position of the Motor for the user
def update(pos):
    text_elem = window["Position"]
    text_elem.update(f"Current Position: {str(pos)}")

#Gets the x and y coordinates when drawing a figure on the canvas
def get_x_and_y(event):
    global lasx, lasy
    lasx, lasy = event.x, event.y
    print(lasx)
    x_c, _ = x_to_steps(lasx/50)
    y_c,_ = y_to_steps(lasy/50)
    draw_path_x.append(x_c)
    draw_path_y.append(y_c)

#Draws user motion on the canvas
def draw_smth(event):
    global lasx, lasy
    canvas.create_oval(lasx, lasy, lasx, lasy, width = 0, fill = 'white')
    lasx, lasy = event.x, event.y
    x_c, _ = x_to_steps(lasx/50)
    y_c,_ = y_to_steps(lasy/50)
    draw_path_x.append(x_c)
    draw_path_y.append(y_c)


def calibration_and_center(joyStick,MotorSys,known_position,board):
    global window
    
    window = sg.Window('Calibration', lay_joystick)
    
    
    while True:
        
        event, values = window.read(timeout=0.1)
        for i in range(1000):
            pass
            #joyStick.control()
        if known_position:
            update(MotorSys.getPosition())
        
        if event in (sg.WIN_CLOSED, 'Cancel'):
            board.sp.close() 
            break
        
        elif event in (sg.WIN_CLOSED, 'Calibrate'):
            position = "0,0"
            update(position)
            known_position = True
            MotorSys.setPosition((0,0))
            
        elif event in (sg.WIN_CLOSED, 'Center'):
            window.close()
            
            MotorSys.center()
            MotorSys.relativeCenter = MotorSys.getPosition()
            window.close()
            
            return True
        
        elif event in (sg.WIN_CLOSED, 'Set Center'):
            window.close()
            MotorSys.setPosition((0,0))
            MotorSys.relativeCenter = MotorSys.getPosition()
            return True

def shape_Choice(board, MotorSys):
    
    global draw_path_x
    global draw_path_y
    global canvas
    
    global window
    
    
    
    window = sg.Window('Cut Wizard', deepcopy(lay_shapeChoice))
    
    draw_path_x = []
    draw_path_y = []
    
    while True:
        event, values = window.read()
        #CHECK WHETHER CANCEL BUTTON HAS BEEN PRESSED
        if event in (sg.WIN_CLOSED, 'Cancel'):
            board.sp.close() 
            window.close()
            break
    
        #CHECK WHETHER OK BUTTON HAS BEEN PRESSED AND CUT HAS BEEN CONFIGURED
        elif event in (sg.WIN_CLOSED, 'OK'):
            cut = True
            
            x_pos,y_pos = MotorSys.relativeCenter
            
            if values['Circle'] == True:
                radius = float(values["radius_input"])
                x_steps, y_steps, path = Shapes.circle(x_pos,y_pos,radius)
                
                if values["Truncated Circle"]:
                    if values["U"]:
                        side = "Left"
                    elif values["L"]:
                        side = "Bottom"
                    elif values["R"]:
                        side = "Top"
                    else:
                        side = "Right"
                    
                    path = Shapes.truncateCircle(x_steps,y_steps,path,side)
                    window.close()
                    return path
                else:
                    window.close()
                    return path
                    
            elif values['Rectangle'] == True:
                x_length = float(values['x length'])
                y_length = float(values['y length'])
                x_steps, y_steps, path = Shapes.rectangle(x_pos,y_pos,x_length,y_length)
                
                if values["Truncated Rectangle"]:
                    if values["TR"]:
                        side = "Top Right"
                    elif values["TL"]:
                        side = "Top Left"
                    elif values["BL"]:
                        side = "Bottom Left"
                    else:
                        side = "Bottom Right"
                    
                    Shapes.truncateRectangle(x_steps,y_steps,path,side)
                    window.close()
                    return path
                else:
                    window.close()
                    return path
            
            elif values['Draw'] == True:
                draw_path_x = np.array(draw_path_x)

                draw_path_y = np.array(draw_path_y)
                draw_path_x = draw_path_x + (MotorSys.relativeCenter[0]-draw_center[0])
                draw_path_y = draw_path_y + (MotorSys.relativeCenter[1]-draw_center[1])
                
                path = LinkedList()
                path.fillList(draw_path_x,draw_path_y,None,None,"Other")
                    
                app.quit()
                window.close()
                return path
    
            window.close()
            break
        
        elif event in (sg.WIN_CLOSED, 'Start Drawing'):
            app = Tk()
            x_length, _ = x_to_steps(float(values['x draw length']))
            y_length, _ = y_to_steps(float(values['y draw length']))
            draw_center = (x_length//2,y_length//2)
            
            app.geometry(f"{int(float(values['x draw length'])*50)}x{int(float(values['x draw length'])*50)}")
            canvas = Canvas(app, bg='black')
            canvas.pack(anchor='nw', fill='both', expand=1)
            canvas.create_oval(draw_center[0], draw_center[1], draw_center[0], draw_center[1], width = 1, fill = 'red')
            canvas.bind("<Button-1>", get_x_and_y)
            canvas.bind("<B1-Motion>", draw_smth)
            app.mainloop()
        
        #CHECK WHETHER CIRCLE OR RECTANGLE HAS BEEN CHOSEN
        #CHECK WHETHER TRUNCATION HAS BEEN CHOSEN
        if values['Circle'] == True:
                
            window['CircleConfiguration'].update(visible=True)
            window['RectangleConfiguration'].update(visible=False)
            window['DrawConfiguration'].update(visible=False)
            
            if values["Truncated Circle"]:
                for key in circle_trunc_radios:
                    window[key].update(visible=True)
                
            else:
                for key in circle_trunc_radios:
                    window[key].update(visible=False)
            
        elif values['Rectangle'] == True:
            
            window['CircleConfiguration'].update(visible=False)
            window['RectangleConfiguration'].update(visible=True)
            window['DrawConfiguration'].update(visible=False)
            
            if values["Truncated Rectangle"]:
                for key in rectangle_trunc_radios:
                    window[key].update(visible=True)
                
            else:
                for key in circle_trunc_radios:
                    window[key].update(visible=False)
        
        elif values['Draw'] == True:
            window['CircleConfiguration'].update(visible=False)
            window['RectangleConfiguration'].update(visible=False)
            window['DrawConfiguration'].update(visible=True)
            
def cut_shape(MotorSys, path, board):
    window = sg.Window('Cutting', deepcopy(lay_cut))
    point = path.start
    continue_cutting = False
    while True:
        
        event, values = window.read(timeout=0.1)
        #CHECK WHETHER CANCEL BUTTON HAS BEEN PRESSED
        if event in (sg.WIN_CLOSED, 'Cancel'):
            board.sp.close() 
            window.close()
            return False
        
        elif event in (sg.WIN_CLOSED, 'Go to Start'):
            point = path.start
            MotorSys.moveTo(point.coord[0],point.coord[1])
            
        elif event in (sg.WIN_CLOSED, "Stop Cutting"):
            continue_cutting = False
            
        elif event in (sg.WIN_CLOSED, "New Shape"):
            x_cen, y_cen = MotorSys.relativeCenter
            MotorSys.moveTo(x_cen,y_cen)
            window.close()
            return True
        
        elif event in (sg.WIN_CLOSED, "Begin") or continue_cutting:
            continue_cutting = True
            for i in range(100):
                point = point.next
                speed = float(values["speed"])
                MotorSys.moveTo(point.coord[0],point.coord[1],speed)
