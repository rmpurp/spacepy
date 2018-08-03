import time
from unittest import TestCase

import card


class TestCard(TestCase):
    def test_rate_card(self):
        t = time.time()
        c = card.Card('d', 'r')

        c.rate_card(0)
        self.assertAlmostEqual(c.easiness_factor, 2.5 - 0.8)
        self.assertAlmostEqual(c.iteration_length, 0)
        self.assertAlmostEqual(t, c.unix_time_to_review, 3)
        self.assertEqual(c.iteration_number, 0)
        self.assertTrue(c.is_reviewable())

        t = time.time()
        c.rate_card(2)
        self.assertAlmostEqual(c.easiness_factor, 2.5 - 0.8)
        self.assertAlmostEqual(c.iteration_length, card.ONE_DAY)
        self.assertAlmostEqual(c.unix_time_to_review, t + card.ONE_DAY, 3)
        self.assertEqual(c.iteration_number, 1)
        self.assertFalse(c.is_reviewable())

        t = time.time()
        c.rate_card(3)
        self.assertAlmostEqual(c.easiness_factor, 2.5 - 0.8 + 0.1)
        self.assertAlmostEqual(c.iteration_length, 6 * card.ONE_DAY)
        self.assertAlmostEqual(c.unix_time_to_review, t + 6 * card.ONE_DAY, 3)
        self.assertFalse(c.is_reviewable())

        t = time.time()
        c.rate_card(2)
        self.assertAlmostEqual(c.easiness_factor, 2.5 - 0.8 + 0.1)
        self.assertAlmostEqual(c.iteration_length,
                               6 * card.ONE_DAY * (2.5 - 0.8 + 0.1))
        self.assertAlmostEqual(c.unix_time_to_review,
                               t + 6 * card.ONE_DAY * (2.5 - 0.8 + 0.1), 3)
        self.assertFalse(c.is_reviewable())

        t = time.time()
        c.rate_card(1)
        self.assertAlmostEqual(c.easiness_factor, 2.5 - 0.8 + 0.1 - 0.3)
        self.assertAlmostEqual(c.iteration_length, 0)
        self.assertAlmostEqual(c.unix_time_to_review, t, 3)
        self.assertTrue(c.is_reviewable())

    '''
    def test_card_equals(self):
        time1 = time.time()
        uuid1 = uuid.uuid1()
        card1 = card.Card('desc1', 'resp1', uuid1, 2.4, time1)
        card2 = card.Card('desc1', 'resp1', uuid1, 2.4, time1)
        card3 = card.Card('desc2', 'resp1', uuid1, 2.4, time1)
        card4 = card.Card('desc1', 'resp2', uuid1, 2.4, time1)
        card5 = card.Card('desc1', 'resp1', uuid.uuid1(), 2.4, time1)
        card6 = card.Card('desc1', 'resp1', uuid1, 2.5, time1)
        card7 = card.Card('desc1', 'resp1', uuid1, 2.4, time.time())
        lst = [card2, card3, card4, card5, card6, card7]
        self.assertEqual(card1, card2)
        for a, b in itertools.combinations(lst, 2):
            self.assertNotEqual(a, b)
    '''
