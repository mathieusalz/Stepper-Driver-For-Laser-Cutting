import pyfirmata
import time
from Circle import circle

board = pyfirmata.Arduino('COM9')

circle(board = board, radius = 8.02, truncated = [False, False])

