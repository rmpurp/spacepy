import tempfile
import unittest

import deck
import file_io


class DeckTest(unittest.TestCase):

    def test_deck_io(self):
        d = deck.create_test_deck()
        with tempfile.TemporaryDirectory() as temp_dir:
            file_io.write_deck(d, temp_dir)
            d2 = file_io.read_deck(path=temp_dir, title='TestDeck')
            self.assertEqual(set(d), set(d2))

    def test_get_reviewable(self):
        d = deck.create_test_deck()

        self.assertEqual(list(d), list(d.reviewable_cards()))

        d[0].rate_card(3)

        self.assertEqual(list(d[1:]), list(d.reviewable_cards()))




if __name__ == '__main__':
    unittest.main()
