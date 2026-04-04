import unittest
from memory_game import MemoryGame

class TestInitialState(unittest.TestCase):
    '''Verify the board is set up correctly when the game is first created.'''

    def setUp(self):
        self.game = MemoryGame()

    def test_score_starts_at_twenty(self):
        '''Score should be 20 at initialization.'''
        self.assertEqual(self.game.score, 20)

    def test_board_contains_sixteen_cards(self):
        '''The colors list should contain exactly 16 entries.'''
        self.assertEqual(len(self.game.colors), 16)

    def test_game_over_is_false(self):
        '''gameOver should be False at initialization.'''
        self.assertFalse(self.game.gameOver)

    def test_matched_set_is_empty(self):
        '''No cards should be in the matched set at initialization.'''
        self.assertEqual(len(self.game.matched), 0)

    def test_flipped_list_is_empty(self):
        '''No cards should be in the flipped list at initialization.'''
        self.assertEqual(len(self.game.flipped), 0)


class TestDeal(unittest.TestCase):
    '''Verify the deck is assembled and shuffled correctly on deal.'''

    def setUp(self):
        self.game = MemoryGame()

    def test_deal_produces_sixteen_cards(self):
        '''deal should always produce exactly 16 cards.'''
        self.game.deal()
        self.assertEqual(len(self.game.colors), 16)

    def test_deal_produces_two_of_each_color(self):
        '''deal should place exactly 2 of each of the 8 colors on the board.'''
        self.game.deal()
        for color in ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'teal']:
            self.assertEqual(self.game.colors.count(color), 2)


class TestCardSelection(unittest.TestCase):
    '''Verify correct return values and state changes when selecting cards.'''

    def setUp(self):
        self.game = MemoryGame()

    def test_first_card_returns_correct_status(self):
        '''Selecting the first card of a turn should return the correct status.'''
        self.assertEqual(self.game.selectCard(0), 'First card flipped')

    def test_first_card_is_added_to_flipped(self):
        '''Selecting a card should add its index to the flipped list.'''
        self.game.selectCard(0)
        self.assertIn(0, self.game.flipped)

    def test_first_card_does_not_decrement_score(self):
        '''Flipping the first card of a turn should not change the score.'''
        self.game.selectCard(0)
        self.assertEqual(self.game.score, 20)


class TestLockedStateBlocking(unittest.TestCase):
    '''Verify that the game logic blocks illegal selections at the logic layer,
    mirroring the protection the UI lock provides at the display layer.'''

    def setUp(self):
        self.game = MemoryGame()

    def test_double_click_same_card_is_blocked(self):
        '''Selecting a card that is already flipped should return the correct block status.'''
        self.game.selectCard(0)
        self.assertEqual(self.game.selectCard(0), 'Card already flipped')

    def test_double_click_does_not_add_duplicate_to_flipped(self):
        '''A blocked double-click should not add the index to flipped a second time.'''
        self.game.selectCard(0)
        self.game.selectCard(0)
        self.assertEqual(self.game.flipped.count(0), 1)

    def test_third_card_blocked_when_two_pending(self):
        '''selectCard should refuse a third selection while two cards are pending.'''
        self.game.flipped = [0, 1]
        self.assertEqual(self.game.selectCard(2), 'Two cards already flipped')

    def test_third_card_not_added_to_flipped(self):
        '''A blocked third-card attempt should not alter the flipped list.'''
        self.game.flipped = [0, 1]
        self.game.selectCard(2)
        self.assertNotIn(2, self.game.flipped)

    def test_third_card_blocked_through_legitimate_first_flip(self):
        '''After flipping one card legitimately, a direct state injection of a
        second entry and then a third click should still be blocked.'''
        self.game.selectCard(5)
        self.game.flipped.append(6)
        self.assertEqual(self.game.selectCard(7), 'Two cards already flipped')

    def test_selecting_card_during_game_over_is_blocked(self):
        '''selectCard should return Game Over and do nothing once gameOver is True.'''
        self.game.gameOver = True
        result = self.game.selectCard(0)
        self.assertEqual(result, 'Game Over')
        self.assertEqual(len(self.game.flipped), 0)


class TestMismatch(unittest.TestCase):
    '''Verify score and state changes when two non-matching cards are selected.'''

    def setUp(self):
        self.game = MemoryGame()
        self.game.colors[0] = 'red'
        self.game.colors[1] = 'blue'

    def test_mismatch_returns_correct_status(self):
        '''A mismatch should return the correct status string.'''
        self.game.selectCard(0)
        self.assertEqual(self.game.selectCard(1), 'No Match')

    def test_mismatch_decrements_score_by_one(self):
        '''A single mismatch should reduce the score by exactly 1.'''
        self.game.selectCard(0)
        self.game.selectCard(1)
        self.assertEqual(self.game.score, 19)

    def test_mismatch_clears_flipped_list(self):
        '''After a mismatch, the flipped list should be empty.'''
        self.game.selectCard(0)
        self.game.selectCard(1)
        self.assertEqual(len(self.game.flipped), 0)

    def test_mismatch_does_not_add_to_matched(self):
        '''Mismatched cards should not be added to the matched set.'''
        self.game.selectCard(0)
        self.game.selectCard(1)
        self.assertNotIn(0, self.game.matched)
        self.assertNotIn(1, self.game.matched)


class TestMatch(unittest.TestCase):
    '''Verify state changes when two matching cards are selected.'''

    def setUp(self):
        self.game = MemoryGame()
        self.game.colors[0] = 'red'
        self.game.colors[1] = 'red'

    def test_match_returns_correct_status(self):
        '''A successful match should return the correct status string.'''
        self.game.selectCard(0)
        self.assertEqual(self.game.selectCard(1), 'Match')

    def test_match_adds_both_indices_to_matched(self):
        '''Both card indices should be in the matched set after a match.'''
        self.game.selectCard(0)
        self.game.selectCard(1)
        self.assertIn(0, self.game.matched)
        self.assertIn(1, self.game.matched)

    def test_match_does_not_decrement_score(self):
        '''A successful match should not change the score.'''
        self.game.selectCard(0)
        self.game.selectCard(1)
        self.assertEqual(self.game.score, 20)

    def test_match_clears_flipped_list(self):
        '''After a match, the flipped list should be empty.'''
        self.game.selectCard(0)
        self.game.selectCard(1)
        self.assertEqual(len(self.game.flipped), 0)

    def test_selecting_matched_card_is_blocked(self):
        '''Attempting to select a card that is already matched should be blocked.'''
        self.game.selectCard(0)
        self.game.selectCard(1)
        self.assertEqual(self.game.selectCard(0), 'Card already matched')


class TestGameOver(unittest.TestCase):
    '''Verify that the game ends correctly when the score reaches zero.'''

    def setUp(self):
        self.game = MemoryGame()
        self.game.colors[0] = 'red'
        self.game.colors[1] = 'blue'

    def test_score_zero_returns_game_over_status(self):
        '''When the final point is lost on a mismatch, Game Over should be returned.'''
        self.game.score = 1
        self.game.selectCard(0)
        self.assertEqual(self.game.selectCard(1), 'Game Over')

    def test_score_zero_sets_game_over_flag(self):
        '''gameOver should be True after the score reaches zero.'''
        self.game.score = 1
        self.game.selectCard(0)
        self.game.selectCard(1)
        self.assertTrue(self.game.gameOver)

    def test_score_zero_clears_flipped_list(self):
        '''The flipped list should be empty after the game ends via score.'''
        self.game.score = 1
        self.game.selectCard(0)
        self.game.selectCard(1)
        self.assertEqual(len(self.game.flipped), 0)

    def test_multiple_mismatches_decrement_score_correctly(self):
        '''Three mismatches should reduce the score from 20 to 17.'''
        for _ in range(3):
            self.game.selectCard(0)
            self.game.selectCard(1)
        self.assertEqual(self.game.score, 17)


class TestWinAndLoss(unittest.TestCase):
    '''Verify isWinner and isLoser return correct values in all states.'''

    def setUp(self):
        self.game = MemoryGame()

    def test_is_not_winner_at_start(self):
        '''isWinner should return False at the start of the game.'''
        self.assertFalse(self.game.isWinner())

    def test_is_winner_when_all_matched(self):
        '''isWinner should return True when all 16 indices are in matched.'''
        self.game.matched = set(range(16))
        self.assertTrue(self.game.isWinner())

    def test_is_not_winner_with_partial_matches(self):
        '''isWinner should return False when only some cards are matched.'''
        self.game.matched = {0, 1, 2, 3}
        self.assertFalse(self.game.isWinner())

    def test_is_not_loser_at_start(self):
        '''isLoser should return False at the start of the game.'''
        self.assertFalse(self.game.isLoser())

    def test_is_loser_when_game_over_flag_set(self):
        '''isLoser should return True when gameOver is True.'''
        self.game.gameOver = True
        self.assertTrue(self.game.isLoser())


class TestReset(unittest.TestCase):
    '''Verify that reset restores the full game state to its initial values.'''

    def setUp(self):
        self.game = MemoryGame()

    def test_reset_restores_score(self):
        '''reset should bring the score back to 20.'''
        self.game.score = 7
        self.game.reset()
        self.assertEqual(self.game.score, 20)

    def test_reset_clears_game_over_flag(self):
        '''reset should set gameOver back to False.'''
        self.game.gameOver = True
        self.game.reset()
        self.assertFalse(self.game.gameOver)

    def test_reset_clears_matched_set(self):
        '''reset should empty the matched set.'''
        self.game.matched = {0, 1, 4, 5}
        self.game.reset()
        self.assertEqual(len(self.game.matched), 0)

    def test_reset_clears_flipped_list(self):
        '''reset should empty the flipped list.'''
        self.game.flipped = [3]
        self.game.reset()
        self.assertEqual(len(self.game.flipped), 0)

    def test_reset_redeals_board(self):
        '''reset should produce a fresh 16-card board.'''
        self.game.reset()
        self.assertEqual(len(self.game.colors), 16)


class TestAccessors(unittest.TestCase):
    '''Verify the accessor methods return correct values.'''

    def setUp(self):
        self.game = MemoryGame()

    def test_get_color_returns_assigned_color(self):
        '''getColor should return the color at the given index.'''
        self.game.colors[7] = 'purple'
        self.assertEqual(self.game.getColor(7), 'purple')

    def test_is_flipped_true_after_selection(self):
        '''isFlipped should return True for a card that has been selected.'''
        self.game.selectCard(4)
        self.assertTrue(self.game.isFlipped(4))

    def test_is_flipped_false_for_unselected(self):
        '''isFlipped should return False for a card that has not been selected.'''
        self.assertFalse(self.game.isFlipped(4))

    def test_is_matched_true_after_match(self):
        '''isMatched should return True for both cards after a successful match.'''
        self.game.colors[0] = 'teal'
        self.game.colors[1] = 'teal'
        self.game.selectCard(0)
        self.game.selectCard(1)
        self.assertTrue(self.game.isMatched(0))
        self.assertTrue(self.game.isMatched(1))

    def test_is_matched_false_for_unmatched(self):
        '''isMatched should return False for a card that has not been matched.'''
        self.assertFalse(self.game.isMatched(2))


if __name__ == '__main__':
    unittest.main()