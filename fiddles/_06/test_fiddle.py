import unittest
from fiddles._06.fiddle import (
    build_orbit_parents,
    count_parents,
    get_checksum,
    get_parents,
    get_first_common_parent,
    count_parents_to,
    count_min_transfers,
)


class TestFiddle(unittest.TestCase):
    def test_build_orbit_parents(self):
        map = [
            ['A', 'B'],
            ['COM', 'A'],
            ['B', 'C']
        ]
        self.assertEqual(
            build_orbit_parents(map),
            {
                'A': 'COM',
                'B': 'A',
                'C': 'B'
            },
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
        map = [
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
            get_checksum(map),
            42
        )

    def test_get_parents(self):
        orbit_parents = {
            'A': 'COM',
            'B': 'A',
            'C': 'B'
        }

        self.assertEqual(
            get_parents(orbit_parents, 'C'),
            ['B', 'A', 'COM']
        )

    def test_get_first_common_parent(self):
        map = [
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
            ['K', 'YOU'],
            ['I', 'SAN'],
        ]

        self.assertEqual(
            get_first_common_parent(build_orbit_parents(map), 'YOU', 'SAN'),
            'D'
        )

    def test_count_parents_to(self):
        map = [
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
            ['K', 'YOU'],
            ['I', 'SAN'],
        ]

        self.assertEqual(
            count_parents_to(build_orbit_parents(map), 'YOU', 'D'),
            3
        )

    def test_count_min_transfers(self):
        map = [
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
            ['K', 'YOU'],
            ['I', 'SAN'],
        ]
        self.assertEqual(
            count_min_transfers(map, 'YOU', 'SAN'),
            4
        )

if __name__ == '__main__':
    unittest.main()
