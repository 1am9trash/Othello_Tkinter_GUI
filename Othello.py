import tkinter as tk
import tkinter.font as font
import numpy as np
from functools import partial


class Othello:
    direction_x = [-1, -1, -1, 0, 0, 1, 1, 1]
    direction_y = [1, 0, -1, 1, -1, -1, 0, 1]

    def __init__(self):
        # 1 white, 2 black, 3 can be choosed
        self.board = self.reset_board()
        self.turn = 1

    def reset_board(self):
        board = np.zeros((8, 8), dtype=int)
        board[3][3] = board[4][4] = 1
        board[3][4] = board[4][3] = 2
        return board

    def check(self, x, y, replace=False):
        flop = np.zeros((8), dtype=bool)
        for i in range(8):
            step = 0
            while True:
                step += 1
                cur_x = x + Othello.direction_x[i] * step
                cur_y = y + Othello.direction_y[i] * step

                if cur_x < 0 or cur_x >= 8 or cur_y < 0 or cur_y >= 8:
                    break
                if self.board[cur_x][cur_y] in [0, 3]:
                    break
                if self.board[cur_x][cur_y] == self.turn:
                    if step == 1:
                        break
                    else:
                        flop[i] = True
                        break

        if not replace:
            return True in flop
        for i in range(8):
            if not flop[i]:
                continue
            step = 0
            while True:
                step += 1
                cur_x = x + Othello.direction_x[i] * step
                cur_y = y + Othello.direction_y[i] * step
                if self.board[cur_x][cur_y] == self.turn:
                    break
                self.board[cur_x][cur_y] = self.turn

    def prepare_move(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != 0:
                    continue
                if self.check(i, j):
                    self.board[i][j] = 3

    def move(self, x, y):
        if self.board[x][y] != 3:
            return
        self.board[x][y] = self.turn
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 3:
                    self.board[i][j] = 0
        self.check(x, y, True)
        self.turn = self.turn % 2 + 1

    def get_status(self):
        return (self.board == 0).sum(), (self.board == 1).sum(), (self.board == 2).sum(), (self.board == 3).sum()


class App:
    color = ["green", "white", "black", "yellow"]

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Othello")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        self.board_frame = tk.Frame(self.root)
        self.board_frame.place(x=0, y=0, width=400, height=400)
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.place(x=200, y=0, width=200, height=400)

        self.game = Othello()

    def render(self):
        self.draw_menu()
        self.draw_board()

    def restart(self):
        self.game.board = self.game.reset_board()
        self.render()

    def draw_menu(self):
        self.menu_frame.destroy()
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.place(x=400, y=0, width=200, height=400)

        but = tk.Button(self.menu_frame, text="Start a new game",
                        font=font.Font(size=15), command=self.restart)
        but.place(x=25, y=25, width=150, height=50)

        message = ""

        empty, white, black, choice = self.game.get_status()
        if empty + choice == 0:
            if white > black:
                message += "White wins\n"
            elif white < black:
                message += "Black wins\n"
            else:
                message += "Draw\n"
        else:
            if self.game.turn == 1:
                message += "White turn\n"
            elif self.game.turn == 2:
                message += "Black turn\n"
        message += \
            "White count: " + str(white) + "\n" + \
            "Black count: " + str(black) + "\n"

        lab = tk.Label(self.menu_frame, text=message,
                       font=font.Font(size=20))
        lab.place(x=25, y=100, width=150)

    def move(self, x, y, event):
        self.game.move(x, y)
        self.render()

    def draw_board(self):
        self.game.prepare_move()

        empty, white, black, choice = self.game.get_status()
        if choice == 0 and empty != 0:
            self.game.turn = self.game.turn % 2 + 1
            self.render()

        self.board_frame.destroy()
        self.board_frame = tk.Frame(self.root)
        self.board_frame.place(width=400, height=400)

        for i in range(8):
            for j in range(8):
                cvs = tk.Canvas(self.board_frame, width=50, height=50,
                                bg="green", highlightthickness=1)
                cvs.place(x=50*i, y=50*j)
                if self.game.board[i][j] in [1, 2]:
                    cvs.create_oval(10, 10, 40, 40,
                                    fill=App.color[self.game.board[i][j]],
                                    width=0)
                elif self.game.board[i][j] == 3:
                    cvs.create_oval(20, 20, 30, 30,
                                    fill=App.color[self.game.board[i][j]],
                                    width=0)
                    cvs.bind("<Button-1>", partial(self.move, i, j))


app = App()
app.render()

app.root.mainloop()
