import serial, time

class BoardMover:
    max_x = 185
    max_y = 1700
    tile_size = 20
    margin__y = 5
    margin__x = 5
    
    def __init__(self, port, baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.ser = serial.Serial(port, baudrate)
        
