# -*- coding: utf-8 -*-
"""
Created on Sat May  6 19:11:55 2023

@author: jsg
"""
import numpy as np
import sys


def quit(b):
    print(f"Your score is {b.sum()} points.")
    sys.exit(0)


def init_board(y_tiles=4, x_tiles=4, start_twos=2):
    """Set initial values on the board, return borad."""
    board = np.zeros((y_tiles, x_tiles)).astype(int)

    for i in range(start_twos):
        z = find_zero(board)
        n = np.random.randint(len(z))
        pos = z[n]
        board[pos[0], pos[1]] = 2
        # print(f"{z=}, {n=}, {pos=}")
    return board

def up(b):    print("up")
def down(b):
    print("down")
    move(b, "down")
    # find_zero(b)
    return b

def left(b):    print("left")
def right(b):    print("right")


def move(board, direction):
    if direction == "down":
        starts = [(3, 0), (3, 1), (3, 2), (3, 3)]
        rel_next = (-1, 0)
    for pos in starts:
        value_here = board[pos[0], pos[1]]
        print(f"{value_here=}")
        pos_nabo = next_pos(pos, rel_next)
        # print(f"{what=}")
        value_nabo = board[pos_nabo[0], pos_nabo[1]]
        if value_here == 0:
            board[pos[0], pos[1]] = value_nabo
            board[pos_nabo[0], pos_nabo[1]] = 0
        else:
            print(str(pos) + str(board[pos[0], pos[1]]))
    return board


def next_pos(pos, rel_next):
    return(pos[0] + rel_next[0], pos[1] + rel_next[1])


def find_zero(board):
    """Find the locations on the board with value zero."""
    return [i for i, e in np.ndenumerate(board) if e == 0]
    # return np.where(board == 0)


# Run program
board = init_board()
print("Welcome to 2048\n"
      + "Make a move ('u', 'd', 'l', 'r'), 'q' to quit.")

while True:
    # print()
    action = input(str(board) + "\n").lower()[0]
    if action == 'u':
        up(board)
    elif action == 'd':
        board = down(board)
    elif action == 'l':
        left(board)
    elif action == 'r':
        right(board)
    elif action == 'q':
        quit(board)
    else:
        print(f" Nope, move {action} is not valid.")

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
