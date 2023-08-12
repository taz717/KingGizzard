from src import boardMover as bm

movelist1= [("B6, B5"),
            ("B5, B4"),
            ("B4, B3")]

BoardMover = bm.BoardMover("COM3", 115200)
BoardMover.demo(movelist1)