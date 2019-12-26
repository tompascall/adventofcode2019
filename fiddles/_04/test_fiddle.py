import unittest
from fiddles._04.fiddle import has_solo_pair, is_increasing, count_candidate


class TestFiddle(unittest.TestCase):

    def test_has_solo_pair(self):
        digits = '123'
        self.assertEqual(
            False,
            has_solo_pair(digits),
            '3 digits with not adjacent pairs'
        )

        digits = '112'
        self.assertEqual(
            True,
            has_solo_pair(digits),
            '3 digits with adjacent pairs'
        )

        digits = '111'
        self.assertEqual(
            False,
            has_solo_pair(digits),
            'three digits with 3 adjacent pairs'
        )

        digits = '11222'
        self.assertEqual(
            True,
            has_solo_pair(digits),
            'adjacent pairs at start'
        )

        digits = '12333'
        self.assertEqual(
            False,
            has_solo_pair(digits),
            'too many pairs at the end'
        )

        digits = '122333'
        self.assertEqual(
            True,
            has_solo_pair(digits),
            'adjacent pairs in the middle'
        )

        digits = '12223'
        self.assertEqual(
            False,
            has_solo_pair(digits),
            'too many pairs in the middle'
        )

        digits = '11122'
        self.assertEqual(
            True,
            has_solo_pair(digits),
            'adjacent pairs at the end'
        )

        digits = '1222'
        self.assertEqual(
            False,
            has_solo_pair(digits),
            'too many pairs at the end'
        )

    def test_is_increasing(self):
        digits = '123'
        self.assertEqual(
            True,
            is_increasing(digits)
        )

        digits = '121'
        self.assertEqual(
            False,
            is_increasing(digits)
        )

    def test_count_candidate(self):
        self.assertEqual(
            2,
            count_candidate(start=119, end=122)
        )


if __name__ == '__main__':
    unittest.main()
