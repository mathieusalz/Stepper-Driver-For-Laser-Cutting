# Stepper-Driver-For-Laser-Cutting

This repository includes all the files necessary to connect your computer to the arduino which controls the stepper motors which move the microscope stage.

## Requirements

Install the required packages by running the command in your command prompt:
```
pip install -r requirements.txt
```

## Running the Code

In order to run the code, all the files need to be located in the same folder. When connecting your computer to the arduino using the USB cable, take note of the COM port used, as line 19 of file gui.py will have to be modified to match the COM port in use. 
```
board = pyfirmata.Arduino('COM{Insert Number Here}}')
```
To open the graphic user interface to control the stepper motors, run the gui.py file from a Python IDE (Spyder, vscode, etc).


## Architecture

### Motor Control

#### joystick.py
Object representing the joystick, which can control the stepper motors to move the stage in x and y

Functions:
- init(board, MotorSys)
- control(self):
- speedMapper(self):

#### Motor.py
Object representing a Motor.

Functions:
- init(dirPin, stepPin):
- run(steps,speed): runs a motor for a given number of steps at a given speed
- setBrother(brother): sets the motors 
- setLimit(limit): sets a limit for the motor 
- switchDirection: switches the direction from the motor (e.g. if set to left then sets to right) 

#### MotorSystem.py
Object representing the Motor System (i.e. the X Motor and Y Motor).

Functions:
##### Setters
- init(board)
- setRelativeCenter(coordinates):
- setPosition(coordinates):
- setLimits():
- setLeft():
- setRight():
- setDown():
- setUp():
##### Getters
- getPosition():
##### Movement
- goLeft(steps):
- goRight(steps):
- goDown(steps):
- goUp(steps):
- center(steps)
- moveTo(x,y,speed)

#### Shapes.py
Script in charge of generating premade shapes.

Functions:
- circle(x_position, y_position, radius):
- truncateCircle():
- rectangle(x_position, y_position, x_length, y_length):
- truncateRectangle():

### User Interface

#### gui.py
Script containing the main workflow for the laser cutting. Intializes the Arduino Board, Motor System, and Joystick. Starts up the graphic user interface and switches between windows (layouts) as required.

#### window.py
Script connecting the front end to the back end.

Functions:
- calibration_and_center(joyStick, MotorSys, board)
- shape_Choice(board, MotorSys):
- cut_shape(MotorSys, path, board):
- chooseConfiguration(window, chosenConfig):
- get_x_and_y(event):
- draw_smt(event):

#### Layouts.py
Script containing the layouts used in window.py

### Miscellaneous

#### helper.py
Script containing the definitions for:
- the range of the x stage and the y stage (69 and 49 millimeters respectively).
- the sensitivity of x motor and y motor per step (2.67 micrometers and 1.67 micrometers respectively)

Functions
- length_to_steps(length,sensitivity):
- x_to_steps(length):
- y_to_steps(length):
- accurate_delay(delay):

#### LinkedList.py
Object representing a singly linked LinkedList datastructure.

Functions:
- init():
- addElement(coordinates):
- fillList(x coordinates, y coordinates):

#### Element.py
Object containing a coordinate position in a path along with the next position to go to. Useful for the Linked List.

Functions:
- init(coordinates)
- setNext(element):


