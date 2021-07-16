import tkinter as tk
import tkinter.font as font
import numpy as np
from functools import partial
import copy
import time


class Othello:
    direction_x = [-1, -1, -1, 0, 0, 1, 1, 1]
    direction_y = [1, 0, -1, 1, -1, -1, 0, 1]
    weight = np.array([[100, 10, 20, 20, 20, 20, 10, 100],
                       [10, -40, -10, -10, -10, -10, -40, 10],
                       [20, -10, 15, 3, 3, 15, -10, 20],
                       [20, -10, 3, 3, 3, 3, -10, 20],
                       [20, -10, 3, 3, 3, 3, -10, 20],
                       [20, -10, 15, 3, 3, 15, -10, 20],
                       [10, -40, -10, -10, -10, -10, -40, 10],
                       [100, 10, 20, 20, 20, 20, 10, 100]])

    def __init__(self):
        # 1 white, 2 black, 3 can be choosed
        self.reset()

    def reset(self, ai=2):
        self.turn = 1
        self.ai = ai
        self.board = np.zeros((8, 8), dtype=int)
        self.board[3][3] = self.board[4][4] = 1
        self.board[3][4] = self.board[4][3] = 2
        self.prepare_move()

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
                if self.board[i][j] == 3:
                    self.board[i][j] = 0
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
        self.prepare_move()

        cant_move, end = self.cant_move_or_end()
        if end == 0 and cant_move:
            self.turn = self.turn % 2 + 1
            self.prepare_move()

    def get_status(self):
        return (self.board == 0).sum(), (self.board == 1).sum(), (self.board == 2).sum(), (self.board == 3).sum()

    def cant_move_or_end(self):
        empty, white, black, choice = self.get_status()
        cant_move = (choice == 0)
        end = 0
        if empty + choice == 0 or white == 0 or black == 0:
            if white > black == 0:
                end = 1
            elif black > white == 0:
                end = 2
            else:
                end = 3
        return cant_move, end

    def heuristic(self):
        white = self.board == 1
        black = self.board == 2
        count = white.sum() + black.sum()
        if white.sum() == 0:
            score = 1000000
        if black.sum() == 0:
            score = -1000000
        else:
            a = (64 - count) / 64
            b = count / 64
            score = ((Othello.weight * a + b) * white).sum() - \
                    ((Othello.weight * a + b) * black).sum()
        if self.ai == 1:
            return score
        else:
            return -score

    def minimax(self, a, b, depth, first=False):
        cant_move, end = self.cant_move_or_end()
        if depth == 0 or end != 0:
            return self.heuristic()
        if self.turn == self.ai:
            x, y, v = -1, -1, -float("inf")
            for i in range(8):
                for j in range(8):
                    if self.board[i][j] == 3:
                        child_node = copy.deepcopy(self)
                        child_node.move(i, j)

                        child_v = child_node.minimax(a, b, depth - 1)
                        if child_v > v:
                            x, y, v = i, j, child_v
                        a = max(a, v)
                        if b <= a:
                            break
        else:
            x, y, v = -1, -1, float("inf")
            for i in range(8):
                for j in range(8):
                    if self.board[i][j] == 3:
                        child_node = copy.deepcopy(self)
                        child_node.move(i, j)

                        child_v = child_node.minimax(a, b, depth - 1)
                        if child_v < v:
                            x, y, v = i, j, child_v
                        b = min(b, v)
                        if b <= a:
                            break
        if first:
            return x, y, v
        return v


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
        if self.game.cant_move_or_end()[1] == 0 and self.game.turn == self.game.ai:
            start = time.time()
            x, y, score = self.game.minimax(-float("inf"), float("inf"),
                                            4, True)
            end = time.time()
            print("    X: {:6d}".format(x))
            print("    Y: {:6d}".format(y))
            print("Score: {:6.2f}".format(score))
            print(" Time: {:6.2f}\n".format(end - start))
            self.move(x, y, None)
        self.draw_menu()
        self.draw_board()

    def restart(self, ai=None):
        self.game.reset(ai)
        self.render()

    def draw_menu(self):
        self.menu_frame.destroy()
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.place(x=400, y=0, width=200, height=400)

        but = tk.Button(self.menu_frame, text="Start a new game",
                        font=font.Font(size=15), command=self.restart)
        but.place(x=25, y=25, width=150, height=50)
        but_ai = tk.Button(self.menu_frame, text="Start a new game\n with AI",
                           font=font.Font(size=15), command=partial(self.restart, 2))
        but_ai.place(x=25, y=100, width=150, height=75)

        message = ""

        empty, white, black, choice = self.game.get_status()
        if empty + choice == 0 or white == 0 or black == 0:
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
        lab.place(x=25, y=200, width=150)

    def move(self, x, y, event):
        self.game.move(x, y)
        self.render()

    def draw_board(self):
        self.board_frame.destroy()
        self.board_frame = tk.Frame(self.root)
        self.board_frame.place(width=400, height=400)

        for i in range(8):
            for j in range(8):
                cvs = tk.Canvas(self.board_frame, width=50, height=50,
                                bg="green", highlightthickness=1)
                cvs.place(x=50*j, y=50*i)
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
