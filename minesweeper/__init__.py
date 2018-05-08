#! /usr/bin/env python3
"""Minesweeper game implmentation."""
import enum
import random
from itertools import product


class TileState(enum.Enum):
    """Represent possible states of tiles."""
    empty = '0'
    mine = 'M'


class Tile:
    """Minesweeper game tile."""

    def __init__(self, state: TileState, clicked: bool):
        self.state = state
        self.clicked = clicked

    def click(self) -> TileState:
        self.clicked = True
        return self.state

    def make_mine(self):
        self.state = TileState.mine

    def get_string(self, cheat=False):
        """Return a visual representation of this tile wrt
        its game state."""
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
        self.x = x
        self.y = y
        self.mines = mines
        self.board = [[Tile(TileState.empty, False) for _x in range(x)]
                      for _y in range(y)]
        # Populate the board with mines by making a list of all coordinates,
        # shuffling it, then getting the first N items of the shuffles list
        all_coords = list(product(range(x), range(y)))
        random.shuffle(all_coords)
        mine_coords = all_coords[:mines]
        # put mines in all renadomaly selected tiles
        for c in mine_coords:
            self.board[c[1]][c[0]].make_mine()

    def flood_click(self, x: int, y: int) -> int:
        # remember visited tiles
        visited_coords = set()
        # stack of tiles to visit in flood fill
        coords_stack = [(x, y)]
        num_clicked = 0
        # flood fill tiles with 0 neighboring mines
        # via recursive depth-first search
        while len(coords_stack) > 0:
            c = coords_stack.pop()
            # ignore any tiles already visited
            if c in visited_coords:
                continue
            visited_coords.add(c)
            my_mines = self.get_num_mines(*c)
            # don't visit this tile's neighbors if there is a mine
            if my_mines != 0:
                continue
            # visit neighbors and add to stack
            for o in NEIGHBOR_OFFSETS:
                c_next = (c[0] + o[0], c[1] + o[1])
                try:
                    # try to click the neighbor
                    self.click(*c_next)
                    coords_stack.append(c_next)
                    num_clicked += 1
                except ValueError:
                    # error occurs when coordinates are off the board.
                    # safe to ignore
                    pass
        return num_clicked

    def move(self, x: int, y: int, autofill: bool = True) -> TileState:
        self._check_coords(x, y)
        t = self.board[y][x]
        if autofill:
            self.flood_click(x, y)
        ret = t.click()
        return ret

    def _check_coords(self, x, y):
        """Throw an error of the given coordinate sare invalid."""
        if any(i < 0 for i in [x, y]):
            raise ValueError('Negative coordinates are invalid!')
        if y >= len(self.board):
            raise ValueError('y larger than board!')
        if x >= len(self.board[0]):
            raise ValueError('x larger than board!')

    def click(self, x, y):
        """Activate the tile at x,y."""
        self._check_coords(x, y)
        self.board[y][x].click()

    def get_num_mines(self, x: int, y: int):
        """Return the number of mines neighboring a tile."""
        self._check_coords(x, y)
        n = 0
        for o in NEIGHBOR_OFFSETS:
            newx = x + o[0]
            newy = y + o[1]
            try:
                self._check_coords(newx, newy)
                if self.board[newy][newx].state == TileState.mine:
                    n += 1
            except ValueError:
                pass

        return n

    def get_string(self, cheat=False):
        """Return an ASCII representation of the baord for console play."""
        rows = []
        # x coords bar
        rows.append(','.join(list(map(str, range(len(self.board[0]))))))
        for y, _ in enumerate(self.board):
            columns = []
            for x, t in enumerate(self.board[y]):
                t = self.board[y][x]
                if t.clicked and t.state != TileState.mine:
                    n = self.get_num_mines(x, y)
                    if n == 0:
                        columns.append(' ')
                    else:
                        columns.append(str(n))

                else:
                    columns.append(t.get_string(cheat=cheat))
            # y coords bar
            columns.append(str(y))
            rows.append('|'.join(columns))
        return '\n'.join(rows)

    def __str__(self):
        return self.get_string(cheat=False)

    def check_win(self):
        """Return whether the player has won the game."""
        count = 0
        for row in self.board:
            for t in row:
                if t.clicked and t.state != TileState.mine:
                    count += 1
        return count == self.x * self.y - self.mines


def main():
    g = Game(10, 10, 5)
    # game input loop
    while True:
        print(g)
        # get user input and handle it if it's invalid
        try:
            x, y = map(int, input('x y >>>').split()[:2])
        except (KeyboardInterrupt, EOFError):
            break
        except ValueError:
            print('Invalid input. Try again.')
            continue
        result = g.move(x, y)
        if result == TileState.mine:
            print('You lose!')
            break
        elif g.check_win():
            print('You win!')
            break

    print(g.get_string(cheat=True))


if __name__ == '__main__':
    main()
