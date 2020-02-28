from unittest.mock import patch
from io import StringIO
import unittest
from fiddles._07.fiddle import (
    execute_next_instruction,
    execute,
    permutations,
    pull_elem,
)


class TestFiddle(unittest.TestCase):
    def test_mul(self):
        program = [0,1002,5,3,5,33]
        result = execute_next_instruction(program, pointer=1)

        self.assertEqual(
            result,
            ([0, 1002, 5, 3, 5, 99], 5)
        )

    def test_add(self):
        program = [0,1001,5,3,5,33]
        result = execute_next_instruction(program, pointer=1)

        self.assertEqual(
            result,
            ([0, 1001, 5, 3, 5, 36], 5)
        )

    def test_halt(self):
        program = [1001,4,3,4,99]
        result = execute_next_instruction(program, pointer=4)

        self.assertEqual(
            result,
            ([1001,4,3,4,99], None)
        )

    def test_store_input(self):
        program = [0,3,2]

        mock_input = ['10']
        with patch('builtins.input', side_effect=mock_input):
            result = execute_next_instruction(program, pointer=1)

        self.assertEqual(
            result,
            ([0, 3, 10], 3)
        )

    def test_output(self):
        program = [0,4,3,50]

        with patch('sys.stdout', new=StringIO()) as fake_output:
            result = execute_next_instruction(program, pointer=1)

        self.assertEqual(
            result,
            ([0,4,3,50], 3)
        )

        self.assertEqual(
            fake_output.getvalue().strip(),
            '50'
        )

    def test_jump_if_true(self):
        program = [0, 5, 0, 2]
        result = execute_next_instruction(program, pointer=1)

        self.assertEqual(
            result,
            (program, 4)
        )

        program = [0, 5, 1, 1]
        result = execute_next_instruction(program, pointer=1)

        self.assertEqual(
            result,
            (program, 5)
        )

        program = [0, 105, 1, 1]
        result = execute_next_instruction(program, pointer=1)

        self.assertEqual(
            result,
            (program, 105)
        )

    def test_jump_if_false(self):
        program = [0, 6, 1, 2]
        result = execute_next_instruction(program, pointer=1)

        self.assertEqual(
            result,
            (program, 4)
        )

        program = [0, 6, 0, 1]
        result = execute_next_instruction(program, pointer=1)

        self.assertEqual(
            result,
            (program, 6)
        )

        program = [0, 106, 0, 1]
        result = execute_next_instruction(program, pointer=1)

        self.assertEqual(
            result,
            (program, 106)
        )


    def test_less_than(self):
        program = [1, 7, 3, 2, 1]
        result = execute_next_instruction(program, pointer=1)

        self.assertEqual(
            result,
            ([1, 1, 3, 2, 1], 5),
            (
                'if the first parameter (position mode) is less than the second parameter, '
                '(position mode) it stores 1 in the position given by the third parameter'
            )
        )

        program = [1, 1107, 2, 3, 1]
        result = execute_next_instruction(program, pointer=1)

        self.assertEqual(
            result,
            ([1, 1, 2, 3, 1], 5),
            (
                'if the first parameter (immediate mode) is less than the second parameter, '
                '(immmediate mode) it stores 1 in the position given by the third parameter'
            )
        )

        program = [1, 7, 1, 2, 1]
        result = execute_next_instruction(program, pointer=1)

        self.assertEqual(
            result,
            ([1, 0, 1, 2, 1], 5),
            (
                'if the first parameter (position mode) is >= the second parameter, '
                '(position mode) it stores 0 in the position given by the third parameter'
            )
        )

        program = [1, 1107, 2, 1, 1]
        result = execute_next_instruction(program, pointer=1)

        self.assertEqual(
            result,
            ([1, 0, 2, 1, 1], 5),
            (
                'if the first parameter (immediate mode) is >= the second parameter, '
                '(immediate mode) it stores 0 in the position given by the third parameter'
            )
        )

    def test_equals(self):
        program = [1, 8, 0, 5, 1, 1]
        result = execute_next_instruction(program, pointer=1)

        self.assertEqual(
            result,
            ([1, 1, 0, 5, 1, 1], 5),
            (
                'if the first parameter (position mode) is equal to the second parameter, '
                '(position mode) it stores 1 in the position given by the third parameter'
            )
        )

        program = [1, 1108, 5, 5, 1, 1]
        result = execute_next_instruction(program, pointer=1)

        self.assertEqual(
            result,
            ([1, 1, 5, 5, 1, 1], 5),
            (
                'if the first parameter (immediate mode) is equal to the second parameter, '
                '(immediate mode) it stores 1 in the position given by the third parameter'
            )
        )

        program = [1, 8, 0, 5, 1, 2]
        result = execute_next_instruction(program, pointer=1)

        self.assertEqual(
            result,
            ([1, 0, 0, 5, 1, 2], 5),
            (
                'if the first parameter (position mode) is not equal to the second parameter, '
                '(position mode) it stores 0 in the position given by the third parameter'
            )
        )

        program = [1, 1108, 5, 4, 1, 1]
        result = execute_next_instruction(program, pointer=1)

        self.assertEqual(
            result,
            ([1, 0, 5, 4, 1, 1], 5),
            (
                'if the first parameter (immediate mode) is not equal to the second parameter, '
                '(immediate mode) it stores 0 in the position given by the third parameter'
            )
        )

    def test_execute(self):
        program = [1002,4,3,4,33]
        result = execute(program)
        self.assertEqual(
            [1002, 4, 3, 4, 99],
            result,
            'Execute the program'
        )

    def test_program_01(self):
        program = [3,9,8,9,10,9,4,9,99,-1,8]

        mock_input = ['8']
        with patch('builtins.input', side_effect=mock_input):
            with patch('sys.stdout', new=StringIO()) as fake_output:
                execute(program)

        self.assertEqual(
            fake_output.getvalue().strip(),
            '1'
        )

    def test_pull_elem(self):
        elems = [1,2,3]

        self.assertEqual(
            pull_elem(elems, 0),
            [1, [2,3]]
        )

    def test_permutations(self):
        input = [1]
        self.assertEqual(
            permutations(input),
            [[1]],
            'One element'
        )

        input = [1, 2]
        tested_permutations = permutations(input)
        expected_permutations = [[2, 1], [1, 2]]

        self.assertEqual(
            len(tested_permutations),
            len(expected_permutations),
            'Two elements'
        )

        for expected_permutation in expected_permutations:
            self.assertEqual(
                expected_permutation in tested_permutations,
                True
            )

        input = [1, 2, 3]
        expected_permutations = [
            [3, 2, 1],
            [2, 3, 1],
            [3, 1, 2],
            [1, 3, 2],
            [2, 1, 3],
            [1, 2, 3]
        ]

        tested_permutations = permutations(input)

        self.assertEqual(
            len(tested_permutations),
            len(expected_permutations),
            'three elements'
        )

        for expected_permutation in expected_permutations:
            self.assertEqual(
                expected_permutation in tested_permutations,
                True
            )

if __name__ == '__main__':
    unittest.main()
