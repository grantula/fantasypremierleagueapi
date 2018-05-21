# -*- coding: utf-8 -*-
"""
File: test_unit_tests.py
Path: fantasypremierleague/tests/
Author: Grant W
"""

import unittest
import fantasypremierleagueapi as fp

class TestEnsureOneItem(unittest.TestCase):

    def setUp(self):
        super().setUp()

    @fp.ensure_one_item
    def fake_func(self, list):
        return list

    def test_ensure_one_item_works(self):
        item = ['1']
        assert self.fake_func(item) == item[0]

    def test_ensure_one_item_raises_error_with_multiples(self):
        item = ['1', '2']
        with self.assertRaises(TypeError):
            self.fake_func(item)

    def test_ensure_one_item_raises_error_with_nothing(self):
        item = []
        with self.assertRaises(TypeError):
            self.fake_func(item)
