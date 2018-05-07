#! /usr/bin/env python3

import enum
import random
from itertools import product


class TileState(enum.Enum):
    empty = '0'
    mine = 'M'


class Tile:
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
        else:
            return '#'

    def __str__(self):
        return self.get_string(cheat=False)


NEIGHBOR_OFFSETS = [(x, y) for x in range(-1, 2) for y in range(-1, 2)
                    if not (x == 0 and y == 0)]


class Game:
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

    def move(self, x: int, y: int):
        t = self.board[y][x]
        return t.click()

    def get_num_mines(self, x: int, y: int):
        n = 0
        for o in NEIGHBOR_OFFSETS:
            try:
                if self.board[y + o[1]][x + o[0]] == TileState.mine:
                    n += 1
            except IndexError:
                pass

    def get_string(self, cheat=False):
        rows = []
        for y,row in enumerate(self.board):
            rows.append('|'.join([t.get_string(cheat=cheat) for t in row]))
        return '\n'.join(rows)

    def __str__(self):
        return self.get_string(cheat=False)


def main():
    g = Game(10, 10, 50)
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
