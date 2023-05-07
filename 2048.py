# -*- coding: utf-8 -*-
"""
Created on Sat May  6 19:11:55 2023

@author: jsg
"""
import numpy as np
import sys
import json


def quit(b):
    score = b.sum()
    print(f"Your score is {score} points.")
    high_score(score)
    sys.exit(0)


def high_score(score):
    with open("high_score.json", "r") as f:
        high = json.load(f)
    yep = False
    if score > int(high["1"][0]):
        yep = True
        name = input("You're the best! New high score.\nWhat's your name? ")
        high["3"] = high["2"]
        high["2"] = high["1"]
        high["1"] = [str(score), name]
    elif score > int(high["2"][0]):
        yep = True
        name = input("You're very good! New high score.\nWhat's your name?  ")
        high["3"] = high["2"]
        high["2"] = [str(score), name]
    elif score > int(high["3"][0]):
        yep = True
        name = input("You're good! New high score.\nWhat's your name?  ")
        high["3"] = [str(score), name]
    if yep:
        print(high)
        with open("high_score.json", "w") as f:
            json.dump(high, f)


def init_board(y_tiles=4, x_tiles=4, start_twos=2):
    """Set initial values on the board, return borad."""
    board = np.zeros((y_tiles, x_tiles)).astype(int)

    for i in range(start_twos):
        board = new(board, lucky=0.9)
    return board


def new(board, lucky=None):
    """Add a new tile to the board."""
    # print(board)
    z = find_zeros(board)
    # print(z)
    n = np.random.randint(len(z))
    pos = z[n]
    if lucky is None:
        lucky = np.random.random()
    if lucky > 0.1:
        board[pos[0], pos[1]] = 2
    else:
        print(f"{lucky=}")
        board[pos[0], pos[1]] = 4
    return board


def move(board, direction):
    """Swipe all tiles to one edge."""
    if direction == "d":
        starts = [(3, 0), (3, 1), (3, 2), (3, 3)]
        rel_next = (-1, 0)
    elif direction == "u":
        starts = [(0, 0), (0, 1), (0, 2), (0, 3)]
        rel_next = (1, 0)
    elif direction == "l":
        starts = [(0, 0), (1, 0), (2, 0), (3, 0)]
        rel_next = (0, 1)
    elif direction == "r":
        starts = [(0, 3), (1, 3), (2, 3), (3, 3)]
        rel_next = (0, -1)
    else:
        sys.exit(1)
    for i in range(3):  # Really board.shape -1
        # Do this 3 times to make sure everything is moved to the edge.
        for pos in starts:
            pos_here = pos
            for n in range(3):  # Really board.shape[0] - 1
                pos_nabo = next_pos(pos_here, rel_next)
                value_here = board[pos_here[0], pos_here[1]]
                # print(f"{pos_here=} {value_here=}")
                value_nabo = board[pos_nabo[0], pos_nabo[1]]
                # print(f"{pos_nabo=} {value_nabo=}")
                if value_here == 0:
                    board[pos_here[0], pos_here[1]] = value_nabo
                    board[pos_nabo[0], pos_nabo[1]] = 0
                else:
                    pass
                # Update positions
                pos_here = next_pos(pos_here, rel_next)
                # print(f"After update: {pos_here=}")
                # print(str(pos) + str(board[pos[0], pos[1]]))
    return board


def add(board, direction):
    """Add equal tiles together in one direction."""
    if direction == "d":
        starts = [(3, 0), (3, 1), (3, 2), (3, 3)]
        rel_next = (-1, 0)
    elif direction == "u":
        starts = [(0, 0), (0, 1), (0, 2), (0, 3)]
        rel_next = (1, 0)
    elif direction == "l":
        starts = [(0, 0), (1, 0), (2, 0), (3, 0)]
        rel_next = (0, 1)
    elif direction == "r":
        starts = [(0, 3), (1, 3), (2, 3), (3, 3)]
        rel_next = (0, -1)
    else:
        sys.exit(1)

    for pos in starts:
        pos_here = pos
        for n in range(3):  # Really board.shape[0] - 1
            pos_nabo = next_pos(pos_here, rel_next)
            value_here = board[pos_here[0], pos_here[1]]
            value_nabo = board[pos_nabo[0], pos_nabo[1]]
            if (not value_here == 0) and (value_here == value_nabo):
                # print(f"{pos_here=} {value_here=}")
                # print(f"{pos_nabo=} {value_nabo=}")
                board[pos_here[0], pos_here[1]] += value_nabo
                pos_nabo2 = next_pos(pos_nabo, rel_next)
                # print(pos_here, pos_nabo, pos_nabo2)
                # print(pos_nabo2, is_on_board(pos_nabo2))
                while is_on_board(pos_nabo2):
                    # for the rest of the tiles in row, move tile along.
                    board[pos_nabo[0], pos_nabo[1]] =\
                        board[pos_nabo2[0], pos_nabo2[1]]
                    # print(board[pos_nabo[0], pos_nabo[1]],
                    #       board[pos_nabo2[0], pos_nabo2[1]])
                    pos_nabo = pos_nabo2
                    pos_nabo2 = next_pos(pos_nabo, rel_next)
                    if not(is_on_board(pos_nabo2)):
                        # If some tiles were moved, the last one is set to zero
                        board[pos_nabo[0], pos_nabo[1]] = 0
            pos_here = next_pos(pos_here, rel_next)
            # print(f"After update: {pos_here=}")
            # print(str(pos) + str(board[pos[0], pos[1]]))
    return board


def next_pos(pos, rel_next):
    return(pos[0] + rel_next[0], pos[1] + rel_next[1])


def is_on_board(pos):
    """Tell if a position is on the board or not."""
    return 0 <= pos[0] <= 3 and 0 <= pos[1] <= 3


def find_zeros(board):
    """Find the locations on the board with value zero."""
    return [i for i, e in np.ndenumerate(board) if e == 0]


# Run program
board = init_board()
print("Welcome to 2048\n"
      + "Make a move ('u', 'd', 'l', 'r'), 'q' to quit.")
legal_moves = [True, True, True, True]
while True:
    direction = input(str(board) + "\n").lower()[0]
    if direction in ['u', 'd', 'l', 'r']:
        old = board.copy()
        board = move(board, direction)
        # print("After moving, but before adding:\n"
        #       + str(board)
        #       + "\nAfter all:")
        board = add(board, direction)
        if (board == old).all():
            # Board did not change, thus move is illegal
            print("Nope, illegal move.")
            if direction == 'u':
                legal_moves[0] = False
            elif direction == 'd':
                legal_moves[1] = False
            elif direction == 'l':
                legal_moves[2] = False
            elif direction == 'r':
                legal_moves[3] = False
            else:
                sys.exit(1)
            if not any(legal_moves):
                print("That's it for now, you lost.")
                quit(board)
            continue  # Don't add another number to the board
        board = new(board)
        # All moves are legal the next time around.
        legal_moves = [True, True, True, True]
    elif direction == 'q':
        quit(board)
    else:
        print(f"Nope, move {direction} is not valid."
              + " Try ('u', 'd', 'l', 'r'), 'q' to quit.")

# Skip GUI for now, makde content

# import tkinter as tk

# class Application(tk.Frame):
#     def __init__(self, master=None):
#         super().__init__(master)
#         self.master = master
#         # self.pack()
#         self.grid()
#         self.create_widgets()

#     def create_widgets(self):
#         self.up = tk.Button(self, text="up", command=self.move_up)
#         self.up.grid(row=0, column=1, columns=3)

#         self.down = tk.Button(self, text="down", command=self.move_down)
#         self.down.grid(row=4, column=1, columns=3)

#         self.left = tk.Button(self, text="left", command=self.move_left)
#         self.left.grid(row=1, rows=3, column=0)

#         self.right = tk.Button(self, text="right", command=self.move_right)
#         # self.right["geometry"] = "100x300"  # Nope
#         self.right.grid(row=1, rows=3, column=4)

#         self.quit = tk.Button(self, text="QUIT", fg="red",
#                               command=self.master.destroy)
#         self.quit.grid(row=4, column=0)

#         self.box1 = tk.Label(self, text="2", bg="#f88")
#         # self.box1["geometry"] = "100x100"  # Nope
#         self.box1.grid(row=1, column=1)
#         self.box2 = tk.Label(self, text="3")
#         self.box2.grid(row=1, column=2)
#         self.box3 = tk.Label(self, text="4")
#         self.box3.grid(row=1, column=3)
#         self.box4 = tk.Label(self, text="5")
#         self.box4.grid(row=2, column=1)
#         self.box5 = tk.Label(self, text="6")
#         self.box5.grid(row=2, column=2)
#         self.box6 = tk.Label(self, text="7")
#         self.box6.grid(row=2, column=3)
#         self.box7 = tk.Label(self, text="8")
#         self.box7.grid(row=3, column=1)
#         self.box8 = tk.Label(self, text="9")
#         self.box8.grid(row=3, column=2)
#         self.box9 = tk.Label(self, text="0")
#         self.box9.grid(row=3, column=3)

#     def move_up(self):
#         print("up")

#     def move_down(self):
#         print("down")

#     def move_left(self):
#         print("left")

#     def move_right(self):
#         print("right")

# root = tk.Tk()
# root.title("2048")
# app = Application(master=root)
# app.mainloop()
