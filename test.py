from src import boardMover as bm

testBoard = bm.BoardMover("COM8", 115200)
command = input("command: ")
while command != "stop":
    match command:
        case "up":
            testBoard.move_relative(0, 10)
        case "down":
            testBoard.move_relative(0, -10)
        case "left":
            testBoard.move_relative(10, 0)
        case "right":
            testBoard.move_relative(-10, 0)
        case "magnet":
            testBoard.start_magnet()
        case "unmagnet":
            testBoard.stop_magnet()
        case "test":
            testBoard.send_gcode("G0 X20 Y20")
        case _:
            x,y = testBoard.board_to_coord(command)
            print(x,y)
            testBoard.move(x,y)
    command = input("command: ")
