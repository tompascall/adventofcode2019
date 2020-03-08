import unittest
from fiddles._08.fiddle import (
    get_layers,
    count_digit_in_layer,
)


class TestFiddle(unittest.TestCase):
    def test_get_layers(self):
        digits = '123456789012'
        layers = get_layers(digits, width=3, height=2)
        self.assertEqual(
            layers,
            [
                [
                    ['1','2','3'],
                    ['4','5','6']
                ],
                [
                    ['7','8','9'],
                    ['0','1','2']
                ]
            ]
        )

    def test_count_digit_in_layer(self):
        digits = '121456789012'
        layers = get_layers(digits, width=3, height=2)
        self.assertEqual(
            count_digit_in_layer(layers[0], '1'),
            2
        )

if __name__ == '__main__':
    unittest.main()
