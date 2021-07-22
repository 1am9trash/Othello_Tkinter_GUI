import tkinter as tk
import tkinter.font as font
from functools import partial
from Othello import Othello
from Minimax import Minimax


class App:
    color = ["green", "white", "black", "yellow"]

    def __init__(self, board_size=8, player1=False, player2=False):
        self.board_size = board_size

        self.root = tk.Tk()
        self.root.title("Othello")
        self.root.geometry(str(50 * board_size + 200) + "x"
                           + str(50 * board_size))
        self.root.resizable(False, False)

        self.board_frame = None
        self.menu_frame = None

        self.game = Othello(board_size)
        self.players = [player1, player2]

        self.render_first = False

    def render(self):
        if self.players[self.game.cur_turn - 1]:
            if not self.render_first:
                self.render_first = True
                self.root.after(1000, self.render)
            else:
                if self.game.cant_move_or_end()[1] == 0:
                    agent = Minimax(self.game.cur_turn)
                    x, y, v = agent.minimax(self.game, -float("inf"), float("inf"),
                                            4, True)
                    self.render_first = False
                    self.move(x, y)
        self.draw_menu()
        self.draw_board()

    def restart(self, player1=False, player2=False):
        self.game.reset(self.board_size)
        self.players = [player1, player2]
        self.render()

    def draw_menu(self):
        if self.menu_frame is not None:
            self.menu_frame.destroy()
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.place(x=str(50 * self.board_size), y=0,
                              width=200, height=str(50 * self.board_size))

        but = tk.Button(self.menu_frame, text="Start a new game",
                        font=font.Font(size=15), command=self.restart)
        but.place(x=25, y=25, width=150, height=50)
        but_ai = tk.Button(self.menu_frame, text="Start a new game\n with AI",
                           font=font.Font(size=15), command=partial(self.restart, False, True))
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
            if self.game.cur_turn == 1:
                message += "White turn\n"
            elif self.game.cur_turn == 2:
                message += "Black turn\n"
        message += \
            "White count: " + str(white) + "\n" + \
            "Black count: " + str(black) + "\n"

        lab = tk.Label(self.menu_frame, text=message,
                       font=font.Font(size=20))
        lab.place(x=25, y=200, width=150)

    def move(self, x, y, event=None):
        self.game.move(x, y)
        self.render()

    def draw_board(self):
        if self.board_frame is not None:
            self.board_frame.destroy()
        self.board_frame = tk.Frame(self.root)
        self.board_frame.place(x=0, y=0,
                               width=str(50 * self.board_size), height=str(50 * self.board_size))

        for i in range(self.board_size):
            for j in range(self.board_size):
                cvs = tk.Canvas(self.board_frame, width=50, height=50,
                                bg="green", highlightthickness=1)
                cvs.place(x=50*j, y=50*i)
                if self.game.state[i][j] in [1, 2]:
                    cvs.create_oval(10, 10, 40, 40,
                                    fill=App.color[self.game.state[i][j]],
                                    width=0)
                elif not self.players[self.game.cur_turn - 1] and self.game.state[i][j] == 3:
                    cvs.create_oval(20, 20, 30, 30,
                                    fill=App.color[self.game.state[i][j]],
                                    width=0)
                    cvs.bind("<Button-1>", partial(self.move, i, j))
