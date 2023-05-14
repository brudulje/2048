# -*- coding: utf-8 -*-
"""
Created on Sat May  6 19:11:55 2023

@author: jsg
"""
import numpy as np
import sys
import json

_legal_moves = [True, True, True, True]
_moves = 0
_directions = {"r": [[(0, 3), (1, 3), (2, 3), (3, 3)], (0, -1)],
               "d": [[(3, 0), (3, 1), (3, 2), (3, 3)], (-1, 0)],
               "l": [[(0, 0), (1, 0), (2, 0), (3, 0)], (0, 1)],
               "u": [[(0, 0), (0, 1), (0, 2), (0, 3)], (1, 0)]
               }
_already_won = False


def main():
    board = init_board()
    print("Welcome to 2048\n"
          + "Make a move ('u', 'd', 'l', 'r'), 'q' to quit.")
    global _legal_moves
    global _moves
    global _directions
    global _already_won

    while True:
        input_ok = False
        while not input_ok:
            keyboard = input(str(board) + "\n")
            if len(keyboard) > 0:
                direction = keyboard.lower()[0]
                input_ok = True
            else:
                print("Invalid input, type at least one character.")

        if direction in ['u', 'd', 'l', 'r']:
            old = board.copy()
            board = move(board, direction)
            # print("After moving, but before adding:\n"
            #       + str(board)
            #       + "\n\nAfter all:", end="")
            board = add(board, direction)
            if (board == old).all():
                # Board did not change, thus move is illegal
                print("Nope, illegal move.")
                if direction == 'u':
                    _legal_moves[0] = False
                elif direction == 'd':
                    _legal_moves[1] = False
                elif direction == 'l':
                    _legal_moves[2] = False
                elif direction == 'r':
                    _legal_moves[3] = False
                else:
                    sys.exit(1)
                if not any(_legal_moves):
                    print("That's it for now, you lost.")
                    quit(board)
                continue  # Don't add another number to the board
            if board.max() > 2000 and not _already_won:
                print("Yay! You won. Weel done.\n"
                      + "Keep going to get an even better high score!!)")
                _already_won = True
            board = new_tile(board)
            # All moves are legal the next time around.
            _legal_moves = [True, True, True, True]
            _moves += 1
        elif direction == 'q':
            quit(board)
        else:
            print(f"Nope, move {direction} is not valid."
                  + " Try ('u', 'd', 'l', 'r'), 'q' to quit.")


def quit(b):
    score = b.sum()
    best = b.max()
    print(f"Your total score is {score} points "
          + f"with a {best} best square, in {_moves} moves.")
    high_score(score, best, _moves)
    sys.exit(0)


def init_board(y_tiles=4, x_tiles=4, start_twos=2):
    """Set initial values on the board, return board."""
    board = np.zeros((y_tiles, x_tiles)).astype(int)

    for i in range(start_twos):
        board = new_tile(board, lucky=0.9)
    return board


def new_tile(board, lucky=None):
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
        # print(f"{lucky=}")
        board[pos[0], pos[1]] = 4
    # print(f"New number at ({pos[0]}, {pos[1]})")
    return board


def move(board, direction):
    """Swipe all tiles to one edge."""
    starts = _directions[direction][0]
    rel_next = _directions[direction][1]

    for i in range(3):  # Really board.shape -1
        for pos in starts:
            pos_here = pos
            for n in range(3):  # Really board.shape - 1
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
    starts = _directions[direction][0]
    rel_next = _directions[direction][1]
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
                # another = True  # Emulate do-while loop
                if not(is_on_board(pos_nabo2)):
                    # If some tiles were moved, the last one is set to zero
                    board[pos_nabo[0], pos_nabo[1]] = 0

                while is_on_board(pos_nabo2):
                    # for the rest of the tiles in row, move tile along.

                    board[pos_nabo[0], pos_nabo[1]] =\
                        board[pos_nabo2[0], pos_nabo2[1]]
                    # print(board[pos_nabo[0], pos_nabo[1]],
                    #       pos_nabo[0], pos_nabo[1],
                    #       board[pos_nabo2[0], pos_nabo2[1]],
                    #       pos_nabo2[0], pos_nabo2[1])
                    pos_nabo = pos_nabo2
                    pos_nabo2 = next_pos(pos_nabo, rel_next)
                    if not(is_on_board(pos_nabo2)):
                        # If some tiles were moved, the last one is set to zero
                        board[pos_nabo[0], pos_nabo[1]] = 0
                    # another = is_on_board(pos_nabo2)
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


def high_score(score, best=2, moves=0):
    """Maintain the top 3 high scores in high_score.json."""
    with open("high_score.json", "r") as f:
        high = json.load(f)
    new_high = False
    if score > int(high["1"][0]):
        new_high = True
        name = input("You're the best! New high score.\nType your name: ")
        high["3"] = high["2"]
        high["2"] = high["1"]
        high["1"] = [str(score), str(best), str(moves), name]
    elif score > int(high["2"][0]):
        new_high = True
        name = input("You're very good! New high score.\nType your name: ")
        high["3"] = high["2"]
        high["2"] = [str(score), str(best), str(moves), name]
    elif score > int(high["3"][0]):
        new_high = True
        name = input("You're good! New high score.\nType your name: ")
        high["3"] = [str(score), str(best), str(moves), name]
    if new_high:
        print(high)
        with open("high_score.json", "w") as f:
            json.dump(high, f)


if __name__ == "__main__":
    main()

# Skip GUI for now, make content

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
