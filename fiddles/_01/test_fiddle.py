import unittest
from fiddles._01.fiddle import RocketModule, Rocket

class TestRocketModule(unittest.TestCase):
    def test_fuel(self):
        test_data = [
            (12, 2, 'It should work for input 12'),
            (14, 2, 'It should work for input 14'),
            (1969, 966, 'It should work for input 1969'),
            (100756, 50346, 'It should work for for input 100756')
        ]

        for data in test_data:
            mass, result, message = data
            rocket_module = RocketModule(mass)
            self.assertEqual(rocket_module.fuel(), result, message)


class TestRocket(unittest.TestCase):
    def test_sum_fuel(self):
        test_data = [
            (['12'], 2, 'It should sum up fuels'),
            (['12', '14'], 4, 'It should sum up fuels')
        ]

        for data in test_data:
            modules, result, message = data
            rocket = Rocket(modules)
            self.assertEqual(rocket.sum_fuel(), result, message)


if __name__ == '__main__':
    unittest.main()
