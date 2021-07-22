import numpy as np


class Othello:
    # 1 白棋, 2 黑棋, 3 下一步可以走
    direction_x = [-1, -1, -1, 0, 0, 1, 1, 1]
    direction_y = [1, 0, -1, 1, -1, -1, 0, 1]

    def __init__(self, board_size=8):
        self.reset(board_size)

    def reset(self, board_size=8):
        # 白棋開始
        self.cur_turn = 1
        # 初始化board
        self.board_size = board_size
        self.state = np.zeros((board_size, board_size), dtype=int)
        l = board_size // 2 - 1
        r = board_size // 2
        self.state[l][l] = self.state[r][r] = 1
        self.state[l][r] = self.state[r][l] = 2
        # 尋找哪些地方可以走
        self.prepare_move()

    def check(self, x, y, replace):
        for i in range(8):
            step = 0
            while True:
                step += 1
                cur_x = x + Othello.direction_x[i] * step
                cur_y = y + Othello.direction_y[i] * step

                if cur_x < 0 or cur_x >= self.board_size or cur_y < 0 or cur_y >= self.board_size:
                    break
                if self.state[cur_x][cur_y] in [0, 3]:
                    break
                if self.state[cur_x][cur_y] == self.cur_turn:
                    if step == 1:
                        break
                    elif replace:
                        for j in range(1, step):
                            temp_x = x + Othello.direction_x[i] * j
                            temp_y = y + Othello.direction_y[i] * j
                            self.state[temp_x][temp_y] = self.cur_turn
                    else:
                        return True
        return False

    def prepare_move(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.state[i][j] in [0, 3] and self.check(i, j, False):
                    self.state[i][j] = 3

    def move(self, x, y):
        if self.state[x][y] != 3:
            return
        self.state[x][y] = self.cur_turn
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.state[i][j] == 3:
                    self.state[i][j] = 0
        self.check(x, y, True)
        self.cur_turn = self.cur_turn % 2 + 1
        self.prepare_move()

        cant_move, end = self.cant_move_or_end()
        if end == 0 and cant_move:
            self.cur_turn = self.cur_turn % 2 + 1
            self.prepare_move()

    def get_status(self):
        return (self.state == 0).sum(), (self.state == 1).sum(), (self.state == 2).sum(), (self.state == 3).sum()

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
