###############################################################################
# This file is in charge of moving the chess pieces on the board. It will
# take in a list of moves and move the pieces accordingly.
###############################################################################

import serial, time

###############################################################################


class BoardMover:
    # BoardMover will make movement using GCODE based on chess moves
    X_MAX = 185
    Y_MAX = 170
    MAGNET_PIN = "P44"

    def __init__(self, port, baudrate=115200, test=False):
        if not test:
            self.serialPort = serial.Serial(port=port, baudrate=baudrate)
            time.sleep(1)
            self.send_gcode("G28")
            # self.serialPort.write(str.encode("G28\r\n"))
            time.sleep(1)
            self.x = 0
            self.y = 0

    def move_relative(self, x, y):
        self.x += x
        self.y += y
        self.send_gcode("G0 X" + str(self.x) + " Y" + str(self.y) + " F2000")
        return

    def move(self, x, y):
        self.x = x
        self.y = y
        self.send_gcode("G0 X" + str(self.x) + " Y" + str(self.y) + " F2000")
        return

    def move_piece(self, origin, destination):
        x, y = self.board_to_coord(origin)
        self.move(x, y)
        time.sleep(3)
        self.start_magnet()
        x, y = self.board_to_coord(destination)
        self.move(x, y)
        time.sleep(3)
        self.stop_magnet()
        return

    def demo(self, plays):
        input("Press Enter to start computer move")
        for play in plays:
            self.move_piece(play[0], play[1])
            input("Press Enter to have computer move")
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
        x_tile = ord(square[0]) - 65
        x = 230 - (x_tile * 30)

        y = (int(square[1]) - 1) * 30 + 20
        return x, y

    def coord_to_board(self, coord):
        return


###############################################################################
