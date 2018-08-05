import os
import tempfile
import unittest

import deck
import file_io


class DeckTest(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)

    def test_deck_io(self):
        d = deck.create_test_deck()
        with tempfile.TemporaryDirectory() as temp_dir:
            file_io.write_deck(d, temp_dir)
            d2 = file_io.read_deck(os.path.join(temp_dir, 'TestDeck'))
            self.assertEqual(set(d), set(d2))


if __name__ == '__main__':
    unittest.main()
