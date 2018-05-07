#! /usr/bin/env python3

import enum
import random
from itertools import product


class TileState(enum.Enum):
    empty = '0'
    mine = 'M'


class Tile:
    """Minesweeper game tile."""

    def __init__(self, state: TileState, clicked: bool):
        self.state = state
        self.clicked = clicked

    def click(self):
        self.clicked = True
        return self.state

    def make_mine(self):
        self.state = TileState.mine

    def get_string(self, cheat=False):
        if self.clicked or cheat:
            return str(self.state.value)
        return '#'

    def __str__(self):
        return self.get_string(cheat=False)


NEIGHBOR_OFFSETS = [(x, y) for x in range(-1, 2) for y in range(-1, 2)
                    if not (x == 0 and y == 0)]


class Game:
    """Minesweeper game implementation."""

    def __init__(self, x: int, y: int, mines: int):
        if mines > x * y:
            raise ValueError(
                'Number of mines can not be greater than size of board!')

        self.board = [[Tile(TileState.empty, False) for _x in range(x)]
                      for _y in range(y)]
        all_coords = list(product(range(x), range(y)))
        random.shuffle(all_coords)
        mine_coords = all_coords[:mines]
        for c in mine_coords:
            self.board[c[1]][c[0]].make_mine()

    def move(self, x: int, y: int, autofill: bool = True):
        seen_coords = set()
        coords_queue = [(x, y)]
        val = 0
        ret = None
        t = self.board[y][x]
        val = t.click()
        if ret is None:
            ret = val
        while len(coords_queue) > 0:
            c = coords_queue.pop()
            # print(c)
            # import pudb
            # pudb.set_trace()
            try:
                if autofill and (c not in seen_coords):
                    for o in NEIGHBOR_OFFSETS:
                        c_next = (c[1] + o[1], c[0] + o[0])
                        if self.get_num_mines(*c_next) == 0:
                            self.board[c_next[1]][c_next[0]].click()
                            coords_queue.append(c_next)
            except IndexError:
                pass
            seen_coords.add(c)
        return ret

    def get_num_mines(self, x: int, y: int):
        n = 0
        for o in NEIGHBOR_OFFSETS:
            try:
                if self.board[y + o[1]][x + o[0]].state == TileState.mine:
                    n += 1
            except IndexError:
                pass
        return n

    def get_string(self, cheat=False):
        rows = []
        # x coords bar
        rows.append(','.join(list(map(str, range(len(self.board[0]))))))
        for y, row in enumerate(self.board):
            row_strings = []
            for x, t in enumerate(self.board[y]):
                t = self.board[y][x]
                if t.clicked and t.state != TileState.mine:
                    row_strings.append(str(self.get_num_mines(x, y)))
                else:
                    row_strings.append(t.get_string(cheat=cheat))
            # y coords bar
            row_strings.append(str(y))
            rows.append('|'.join(row_strings))
        return '\n'.join(rows)

    def __str__(self):
        return self.get_string(cheat=False)


def main():
    g = Game(10, 10, 3)
    # game input loop
    while True:
        print(g)
        try:
            x, y = map(int, input('x y >>>').split(' ')[:2])
        except (KeyboardInterrupt, EOFError):
            break
        except ValueError:
            print('Invalid input. Try again.')
            continue
        result = g.move(x, y)
        if result == TileState.mine:
            print('You lose!')
            break

    print(g.get_string(cheat=True))


if __name__ == '__main__':
    main()
