# Stepper-Driver-For-Laser-Cutting

This repository includes all the files necessary to connect your computer to the arduino which controls the stepper motors which move the microscope stage.

## Requirements

The following python libraries will be needed:
- numpy
- matplotlib
- pyfirmata
- tkinter
- PySimpleGUI
- PIL

## Running the Code

In order to run the code, all the files need to be located in the same folder. When connecting your computer to the arduino using the USB cable, take note of the COM port used, as line 28 of file gui.py will have to be modified to match the COM port in use. To open the graphic user interface to control the stepper motors, run the gui.py file from a Python IDE (Spyder, vscode, etc).


