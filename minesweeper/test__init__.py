import unittest
import minesweeper


def et():
    """Return a new instance of an empty tile."""
    return minesweeper.Tile(state=minesweeper.TileState.empty, clicked=False)


def mt():
    """Return a new instance of a mine tile."""
    return minesweeper.Tile(state=minesweeper.TileState.mine, clicked=False)


class MineSweeperTests(unittest.TestCase):

    def test_count_mines(self):
        g = minesweeper.Game(2, 2, 1)
        g.board = [
            [et(), et()],
            [et(), mt()],
        ]
        self.assertEqual(g.get_num_mines(0, 0), 1)
        self.assertEqual(g.get_num_mines(1, 0), 1)
        self.assertEqual(g.get_num_mines(0, 1), 1)
        self.assertEqual(g.get_num_mines(1, 1), 0)
        g.board = [
            [mt(), et()],
            [et(), mt()],
        ]
        self.assertEqual(g.get_num_mines(0, 0), 1)
        self.assertEqual(g.get_num_mines(1, 0), 2)
        self.assertEqual(g.get_num_mines(0, 1), 2)
        self.assertEqual(g.get_num_mines(1, 1), 1)
        g = minesweeper.Game(3, 3, 1)
        g.board = [
            [et(), et(), et()],
            [et(), mt(), et()],
            [et(), et(), et()],
        ]
        self.assertEqual(g.get_num_mines(0, 0), 1)
        self.assertEqual(g.get_num_mines(1, 1), 0)
        self.assertEqual(g.get_num_mines(2, 2), 1)
        self.assertEqual(g.get_num_mines(0, 2), 1)
        self.assertEqual(g.get_num_mines(1, 2), 1)

    def test_flood_click(self):
        g = minesweeper.Game(2, 2, 1)
        g.board = [
            [et(), et()],
            [et(), mt()],
        ]
        g.flood_click(0, 0)
        self.assertTrue(g.get_tile(0, 0).clicked)
        self.assertFalse(g.get_tile(0, 1).clicked)
        self.assertFalse(g.get_tile(1, 0).clicked)
        self.assertFalse(g.get_tile(1, 1).clicked)
        g = minesweeper.Game(3, 3, 1)
        g.board = [
            [et(), et(), et()],
            [et(), mt(), et()],
            [et(), et(), et()],
        ]
        clicked_mask = [
            [True, False, False],
            [False, False, False],
            [False, False, False],
        ]
        g.flood_click(0, 0)
        for brow, crow in zip(g.board, clicked_mask):
            for bcol, ccol in zip(brow, crow):
                self.assertEqual(bcol.clicked, ccol)

        g = minesweeper.Game(3, 3, 1)
        g.board = [
            [et(), et(), et()],
            [et(), et(), et()],
            [et(), et(), mt()],
        ]
        clicked_mask = [
            [True, True, True],
            [True, True, True],
            [True, True, False],
        ]
        g.flood_click(0, 0)
        for brow, crow in zip(g.board, clicked_mask):
            for bcol, ccol in zip(brow, crow):
                self.assertEqual(bcol.clicked, ccol)
