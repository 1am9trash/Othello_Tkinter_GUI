import numpy as np
from Othello import Othello
import copy


class Minimax:
    weight = np.array([[100, 10, 20, 20, 20, 20, 10, 100],
                       [10, -40, -10, -10, -10, -10, -40, 10],
                       [20, -10, 15, 3, 3, 15, -10, 20],
                       [20, -10, 3, 3, 3, 3, -10, 20],
                       [20, -10, 3, 3, 3, 3, -10, 20],
                       [20, -10, 15, 3, 3, 15, -10, 20],
                       [10, -40, -10, -10, -10, -10, -40, 10],
                       [100, 10, 20, 20, 20, 20, 10, 100]])

    def __init__(self, agent_turn):
        self.agent_turn = agent_turn

    def heuristic(self, game):
        white = game.state == 1
        black = game.state == 2
        count = white.sum() + black.sum()

        if white.sum() == 0:
            score = 1000000
        elif black.sum() == 0:
            score = -1000000
        else:
            if game.board_size == 8:
                a = (64 - count) / 64
                b = count / 64
                score = ((Minimax.weight * a + b) * white).sum() - \
                        ((Minimax.weight * a + b) * black).sum()
            else:
                score = white.sum() - black.sum()
        if self.agent_turn == 1:
            return score
        else:
            return -score

    def minimax(self, game, a, b, depth, first=False):
        cant_move, end = game.cant_move_or_end()
        if depth == 0 or end != 0:
            return self.heuristic(game)
        if self.agent_turn == game.cur_turn:
            x, y, v = -1, -1, -float("inf")
            for i in range(game.board_size):
                for j in range(game.board_size):
                    if game.state[i][j] == 3:
                        child_node = copy.deepcopy(game)
                        child_node.move(i, j)

                        child_v = self.minimax(child_node, a, b, depth - 1)
                        if child_v > v:
                            x, y, v = i, j, child_v
                        a = max(a, v)
                        if b <= a:
                            break
        else:
            x, y, v = -1, -1, float("inf")
            for i in range(game.board_size):
                for j in range(game.board_size):
                    if game.state[i][j] == 3:
                        child_node = copy.deepcopy(game)
                        child_node.move(i, j)

                        child_v = self.minimax(child_node, a, b, depth - 1)
                        if child_v < v:
                            x, y, v = i, j, child_v
                        b = min(b, v)
                        if b <= a:
                            break
        if first:
            return x, y, v
        return v
