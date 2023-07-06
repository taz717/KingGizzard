import serial, time

class BoardMover:
    #BoardMover will make movement using GCODE based on chess moves
    x_max = 185
    y_max = 170

    def __init__(self, port, baudrate=115200):
        self.serialPort = serial.Serial(port = port, baudrate = baudrate)
        time.sleep(1)
        self.serialPort.write(str.encode("G28\r\n"))

    def move_piece(self, origin, destination):
        return
    
    def take_piece(self, origin):
        return
    
    def send_gcode(self, gcode):
        self.serialPort.write(str.encode(gcode + "\r\n"))
        return

board = BoardMover("COM8")
board.send_gcode("G1 X185 Y170")
