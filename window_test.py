# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 18:04:42 2023

@author: mathi
"""
import PySimpleGUI as sg
import Shapes
import numpy as np
from helper import x_to_steps, y_to_steps
from copy import deepcopy
from LinkedList import LinkedList
import layouts
from tkinter import Tk, Canvas


circle_trunc_radios = ["U","L","D","R"]
rectangle_trunc_radios = ["TL","TR","BR","BL"]
configurations = ["CircleConfiguration","RectangleConfiguration","DrawConfiguration"]


#Gets the x and y coordinates when drawing a figure on the canvas
def get_x_and_y(event):
    global lasx, lasy
    lasx, lasy = event.x, event.y
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


def calibration_and_center():
    global window
    
    window = sg.Window('Calibration', layouts.lay_joystick)
    
    
    while True:
        
        event, values = window.read(timeout=0.1)
        
        #   Cancel
        if event in (sg.WIN_CLOSED, 'Cancel'):
            window.close()
            break
        
        #   Calibrate
        elif event in (sg.WIN_CLOSED, 'Calibrate'):
            pass
        
        #   Center
        elif event in (sg.WIN_CLOSED, 'Center'):
            window.close()
            return True
        
        #   Set Center
        elif event in (sg.WIN_CLOSED, 'Set Center'):
            return True

def shape_Choice():

    global draw_path_x
    global draw_path_y
    global canvas
    global window
    
    window = sg.Window('Cut Wizard', deepcopy(layouts.lay_shapeChoice))
    
    draw_path_x = []
    draw_path_y = []
    
    while True:
        event, values = window.read()
        
        #   Cancel
        if event in (sg.WIN_CLOSED, 'Cancel'):
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
    
        #   Ok
        elif event in (sg.WIN_CLOSED, 'OK'):
            
            x_pos,y_pos = (0,0)
            
            #   Circle
            if values['Circle'] == True:
                radius = float(values["radius_input"])
                x_steps, y_steps, path = Shapes.circle(x_pos,y_pos,radius)
                
                # Truncation
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
            
            #   Rectangle
            elif values['Rectangle'] == True:
                x_length = float(values['x length'])
                y_length = float(values['y length'])
                x_steps, y_steps, path = Shapes.rectangle(x_pos,y_pos,x_length,y_length)
                
                #   Truncation
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
            
            #   Draw
            elif values['Draw'] == True:
                draw_path_x = np.array(draw_path_x)

                draw_path_y = np.array(draw_path_y)
                draw_path_x = draw_path_x + (0-draw_center[0])
                draw_path_y = draw_path_y + (0-draw_center[1])
                
                path = LinkedList()
                path.fillList(draw_path_x,draw_path_y,None,None,"Other")
                
                app.destroy()
                window.close()
                return path
    
            window.close()
            break
        

        '''
        RadioButtons - Determine Layout Needed
        '''
        
        #   Cirle RadioButton
        if values['Circle'] == True:
            chooseConfiguration(window,"CircleConfiguration")
            
            # Truncation Checkbox
            if values["Truncated Circle"]:
                for key in circle_trunc_radios:
                    window[key].update(visible=True)
                
            else:
                for key in circle_trunc_radios:
                    window[key].update(visible=False)
        
        #   Rectangle Radiobutton
        elif values['Rectangle'] == True:
            chooseConfiguration(window,"RectangleConfiguration")
            
            #Truncation Checkbox
            if values["Truncated Rectangle"]:
                for key in rectangle_trunc_radios:
                    window[key].update(visible=True)
                
            else:
                for key in circle_trunc_radios:
                    window[key].update(visible=False)
        
        #   Draw Radiobutton
        elif values['Draw'] == True:
            chooseConfiguration(window,"DrawConfiguration")
            
def cut_shape(path):
    
    window = sg.Window('Cutting', deepcopy(layouts.lay_cut))
    point = path.start
    continue_cutting = False
    
    while True:
        
        event, values = window.read(timeout=0.1)
        
        #   CANCEL
        if event in (sg.WIN_CLOSED, 'Cancel'):
            window.close()
            return False
       
        #   Go to Start
        elif event in (sg.WIN_CLOSED, 'Go to Start'):
            pass
            
        #   Stop Cutting
        elif event in (sg.WIN_CLOSED, "Stop Cutting"):
            continue_cutting = False
        
        #   New Shape
        elif event in (sg.WIN_CLOSED, "New Shape"):
            window.close()
            return True
        
        #   Begin
        elif event in (sg.WIN_CLOSED, "Begin") or continue_cutting:
            continue_cutting = True
            for i in range(100):
                point = point.next
          
                
def chooseConfiguration(window,chosenConfig):
    for config in configurations:
        if config == chosenConfig:
            window[config].update(visible=True)
        else:
            window[config].update(visible=False)
    