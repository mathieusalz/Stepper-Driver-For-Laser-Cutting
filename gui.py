'''
########################################################################
                                IMPORTS
########################################################################
'''

import pyfirmata
from MotorSystem import Motor_System
from joyStick import JoyStick
from window import calibration_and_center, shape_Choice, cut_shape


'''
########################################################################
                            INITIALIZATIONS
########################################################################
'''

board = pyfirmata.Arduino('COM9')
MotorSys = Motor_System(board)
joyStick = JoyStick(board,MotorSys)


'''
########################################################################
                                WORKFLOW
########################################################################
'''

cut_wizard = calibration_and_center( 
                                    joyStick = joyStick, 
                                    MotorSys = MotorSys, 
                                    board = board
                                    )
while cut_wizard:
    
    path, recalibrate = shape_Choice( 
                 board = board,
                 MotorSys = MotorSys
                 )

    if recalibrate:
        cut_wizard = calibration_and_center( 
                                            joyStick = joyStick, 
                                            MotorSys = MotorSys, 
                                            board = board
                                            )        
    elif path is not None:
        
        cut_wizard = cut_shape(
            MotorSys, 
            path,
            board
            )
    else:
        break

'''
########################################################################
                                    PROGRAM END
########################################################################
'''      
        
board.sp.close()