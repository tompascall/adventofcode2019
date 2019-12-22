import unittest
from fiddles._03.fiddle import get_route, tokens_to_coords


class TestFiddle(unittest.TestCase):

    def test_get_route_rigth(self):
        origo = (0, 0)
        token = 'R2'
        self.assertEqual(
            [(1, 0), (2, 0)],
            get_route(origo, token),
            'Get route from R2'
        )

    def test_get_route_left(self):
        origo = (0, 0)
        token = 'L2'
        self.assertEqual(
            [(-1, 0), (-2, 0)],
            get_route(origo, token),
            'Get route from L2'
        )

    def test_get_route_up(self):
        origo = (0, 0)
        token = 'U2'
        self.assertEqual(
            [(0, 1), (0, 2)],
            get_route(origo, token),
            'Get route from U2'
        )

    def test_get_route_down(self):
        origo = (0, 0)
        token = 'D2'
        self.assertEqual(
            [(0, -1), (0, -2)],
            get_route(origo, token),
            'Get route from D2'
        )

    def test_tokens_to_coords(self):
        tokens = ['R2','U2','L2','D2']
        self.assertEqual(
            tokens_to_coords(tokens, (0, 0)),
            [
                (0, 0),
                (1, 0), (2, 0),
                (2, 1), (2, 2),
                (1, 2), (0, 2),
                (0, 1), (0, 0)
            ],
            'Form route coords from tokens'
        )

if __name__ == '__main__':
    unittest.main()
