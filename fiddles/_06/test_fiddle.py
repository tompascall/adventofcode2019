import unittest
from fiddles._06.fiddle import (
    build_orbit_parents,
    count_parents,
    get_checksum,
)


class TestFiddle(unittest.TestCase):
    def test_build_orbit_parents(self):
        input = [
            ['A', 'B'],
            ['COM', 'A'],
            ['B', 'C']
        ]
        self.assertEqual(
            build_orbit_parents(input),
            {
                'A': 'COM',
                'B': 'A',
                'C': 'B'
            },
            'Building orbit parents'
        )

    def test_count_parents(self):
        orbit_parents = {
            'A': 'COM',
            'B': 'A',
            'C': 'B'
        }
        self.assertEqual(
            count_parents(orbit_parents, 'A'),
            1
        )

        self.assertEqual(
            count_parents(orbit_parents, 'B'),
            2,
        )

    def test_get_checksum(self):
        input = [
            ['COM', 'B'],
            ['B', 'C'],
            ['C', 'D'],
            ['D', 'E'],
            ['E', 'F'],
            ['B', 'G'],
            ['G', 'H'],
            ['D', 'I'],
            ['E', 'J'],
            ['J', 'K'],
            ['K', 'L'],
        ]

        self.assertEqual(
            get_checksum(input),
            42
        )

if __name__ == '__main__':
    unittest.main()
