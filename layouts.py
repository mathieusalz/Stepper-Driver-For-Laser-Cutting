# -*- coding: utf-8 -*-
"""
Created on Wed May  3 16:50:45 2023

@author: mathi
"""

import PySimpleGUI as sg

'''                            
                                ***************   
                                Calibration Layout
                                ***************
'''

lay_joystick= [[sg.Text('Calibrate and Center:')],
          [sg.Button('Calibrate'),
           sg.Button('Center'),
           sg.Button('Set Center'),
           sg.Button("Cancel")]]


'''                               
                                ***************
                            Shape Configuration - Circle Layout
                                ***************
'''

lay_circle = [[sg.Text('Circle')],
            [sg.Text('Enter Circle radius'), sg.InputText(key="radius_input")],
            [sg.Checkbox("Truncated",key="Truncated Circle",enable_events=True)],
            [sg.Radio('Top','sides', key ='U',visible= False,enable_events=True), 
             sg.Radio('Left','sides', key='L',visible= False,enable_events=True),
             sg.Radio('Bottom','sides', key ='D',visible= False,enable_events=True),
             sg.Radio('Right','sides', key ='R',visible= False,enable_events=True)
             ]]

'''                               
                                ***************
                            Shape Configuration - Rectangle Layout
                                ***************
'''

lay_rectangle = [[sg.Text('Rectangle')],
            [sg.Text('Enter X length'), sg.InputText(key="x length")],
            [sg.Text('Enter Y length'), sg.InputText(key='y length')],
            [sg.Checkbox("Truncated",key="Truncated Rectangle",enable_events=True)],
            [sg.Radio('Top Right','corners', key ='TR',visible= False,enable_events=True), 
             sg.Radio('Top Left','corners', key='TL',visible= False,enable_events=True),
             sg.Radio('Bottom Right','corners', key ='BR',visible= False,enable_events=True),
             sg.Radio('Bottom Left','corners', key ='BL',visible= False,enable_events=True)
             ]]

'''                               
                                ***************
                            Shape Configuration -Drawing Layout
                                ***************
'''

lay_draw = [[sg.Text('Drawing Parameters')],
            [sg.Text('Enter X length'), sg.InputText(key="x draw length")],
            [sg.Text('Enter Y length'), sg.InputText(key='y draw length')],
            [sg.Button("Start Drawing")]
            ]

'''                               
                                ***************
                            Shape Configuration Layout
                                ***************
'''

lay_shapeChoice = [[sg.Text('Choose a shape:')],
          [sg.Radio('Circle','shapes', key ='Circle', enable_events=True), 
           sg.Radio('Rectangle','shapes', key='Rectangle', enable_events=True),
           sg.Radio('Draw', 'shapes', key='Draw', enable_events=True)],
          [sg.Column(lay_circle, key='CircleConfiguration', visible= False), 
           sg.Column(lay_rectangle, visible=False, key='RectangleConfiguration'),
           sg.Column(lay_draw, visible=False, key='DrawConfiguration')],
          [sg.Button('OK'),sg.Button('Cancel')]]


'''                               
                                ***************
                                 Cutting Layout
                                ***************
'''

lay_cut = [[sg.Text('Ready to Cut:')],
          [sg.Button('Go to Start'),
           sg.Button('Begin'),
           sg.Button("Stop Cutting"),
           sg.Button("New Shape"),
           sg.Button("Cancel")],
          [sg.Slider(range=(0.1,1), default_value=1, resolution = 0.01, 
                     orientation='horizontal',enable_events=True,key="speed")]]