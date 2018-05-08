import unittest
import minesweeper

empty_tile = minesweeper.Tile(state=minesweeper.TileState.empty, clicked=False)
mine_tile = minesweeper.Tile(state=minesweeper.TileState.mine, clicked=False)


class MineSweeperTests(unittest.TestCase):
    def test_count_mines(self):
        g = minesweeper.Game(2, 2, 1)
        g.board = [
            [empty_tile, empty_tile],
            [empty_tile, mine_tile],
        ]
        self.assertEqual(g.get_num_mines(0, 0), 1)
        self.assertEqual(g.get_num_mines(1, 0), 1)
        self.assertEqual(g.get_num_mines(0, 1), 1)
        self.assertEqual(g.get_num_mines(1, 1), 0)
