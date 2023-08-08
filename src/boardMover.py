import serial, time

class BoardMover:
    #BoardMover will make movement using GCODE based on chess moves
    X_MAX = 185
    Y_MAX = 170
    MAGNET_PIN = "P44"


    def __init__(self, port, baudrate=115200, test=False):
        if not test:
            self.serialPort = serial.Serial(port = port, baudrate = baudrate)
            time.sleep(1)
            self.send_gcode("G28")
            #self.serialPort.write(str.encode("G28\r\n"))
            time.sleep(1)
            self.x = 0
            self.y = 0

    def move_relative(self, x, y):
        self.x += x
        self.y += y
        self.send_gcode("G0 X" + str(self.x) + " Y" + str(self.y))
        return
    def move(self, x, y):
        self.x = x
        self.y = y
        self.send_gcode("G0 X" + str(self.x) + " Y" + str(self.y))
        return
    
    def move_piece(self, origin, destination):
        self.move(self.board_to_coord(origin))
        self.start_magnet()
        self.move(self.board_to_coord(destination))
        self.stop_magnet()
        return
    
    def take_piece(self, origin):
        return
    
    def send_gcode(self, gcode):
        self.serialPort.write((gcode + "\n").encode())
        time.sleep(1)
        return

    def start_magnet(self):
        self.send_gcode("M42 " + self.MAGNET_PIN + " S255")
        return
    def stop_magnet(self):
        self.send_gcode("M42 " + self.MAGNET_PIN + " S0")
        return
    
    def board_to_coord(self, square):
        x =  160 - (ord(square[0]) - 65) *20
        y = int(square[1]) * 20
        return x, y
    
    def coord_to_board(self, coord):
        return