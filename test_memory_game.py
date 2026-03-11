import unittest
from memory_game import MemoryGame

class TestMemoryGame(unittest.TestCase):
    def setUp(self):
        self.game = MemoryGame()

    def test_initial_state(self):
        self.assertEqual(self.game.score, 20)
        self.assertEqual(len(self.game.colors), 16)
        self.assertFalse(self.game.gameOver)

    def test_select_card(self):
        self.assertEqual(self.game.selectCard(0), 'First card flipped')