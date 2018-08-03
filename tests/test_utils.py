import json
import time
from unittest import TestCase

import card
import utils


class TestUtils(TestCase):

    def test_json(self):
        t = time.time()
        c = card.Card('This is a description\nNew Line',
                      'This is a response\na',
                      easiness_factor=2.3)
        dump = json.dumps(c, default=utils.json_default)
        print(
            json.dumps(c, default=utils.json_default, sort_keys=True, indent=4))
        load = json.loads(dump, object_hook=utils.json_object_hook)
        self.assertEqual(c.__dict__, load.__dict__)
        self.assertAlmostEqual(c.time_created, load.time_created)
        self.assertAlmostEqual(c.time_created, t, 3)

    def test_merge_one_layer(self):
        a = {1: 1, 2: 2, 3: 3}
        b = {1: 2, 2: 1, 3: 3}
        merged = utils.recursive_dict_merge(a, b)
        self.assertEqual(merged, {1: 2, 2: 2, 3: 3})
        merged = utils.recursive_dict_merge(a, b, lambda d, k: -d[k])
        self.assertEqual(merged, {1: 1, 2: 1, 3: 3})

    def test_merge_two_layers(self):
        a = {1: 1, 2: 2, 3: 3}
        b = {1: 2, 2: 1, 3: 3}
        a[4] = dict(a)
        b[4] = dict(b)
        invert = lambda d, k: -d[k]
        merged = utils.recursive_dict_merge(a, b)
        self.assertEqual(merged, {1: 2, 2: 2, 3: 3, 4: {1: 2, 2: 2, 3: 3}})

        merged = utils.recursive_dict_merge(a, b, invert)
        self.assertEqual(merged, {1: 1, 2: 1, 3: 3, 4: {1: 2, 2: 2, 3: 3}})

        merged = utils.recursive_dict_merge(a, b, invert, invert)
        self.assertEqual(merged, {1: 1, 2: 1, 3: 3, 4: {1: 1, 2: 1, 3: 3}})
