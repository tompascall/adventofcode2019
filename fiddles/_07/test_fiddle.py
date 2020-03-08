import unittest
from fiddles._07.fiddle import (
    permutations,
    pull_elem,
    execute_next_instruction,
    execute,
    IO,
    Machine,
    execute_connected_programs
)


class TestFiddle(unittest.TestCase):
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

    def test_mul(self):
        program = [0,1002,5,3,5,33]
        io = IO()
        result = execute_next_instruction(program, pointer=1, io=io)

        self.assertEqual(
            result,
            ([0, 1002, 5, 3, 5, 99], 5, io),
        )

    def test_add(self):
        program = [0,1001,5,3,5,33]
        io = IO()
        result = execute_next_instruction(program, pointer=1, io=io)

        self.assertEqual(
            result,
            ([0, 1001, 5, 3, 5, 36], 5, io)
        )

    def test_halt(self):
        program = [1001,4,3,4,99]
        io = IO()
        result = execute_next_instruction(program, pointer=4, io=io)

        self.assertEqual(
            result,
            ([1001,4,3,4,99], None, io)
        )

    def test_store_input(self):
        program = [0,3,2]
        io = IO(initial_io={ 'input': ['10'], 'output': [] })
        result = execute_next_instruction(program, pointer=1, io=io)

        self.assertEqual(
            result,
            ([0, 3, 10], 3, io),
        )

    def test_output(self):
        program = [0,4,3,50]
        io = IO(initial_io={ 'input': [], 'output': [] })
        result = execute_next_instruction(program, pointer=1, io=io)

        self.assertEqual(
            result,
            ([0,4,3,50], 3, io)
        )

        self.assertEqual(
            io.get_next_output(),
            '50'
        )

    def test_jump_if_true(self):
        program = [0, 5, 0, 2]
        io = IO()
        result = execute_next_instruction(program, pointer=1, io=io)

        self.assertEqual(
            result,
            (program, 4, io),
        )

        program = [0, 5, 1, 1]
        io = IO()
        result = execute_next_instruction(program, pointer=1, io=io)

        self.assertEqual(
            result,
            (program, 5, io),
        )

        program = [0, 105, 1, 1]
        io = IO()
        result = execute_next_instruction(program, pointer=1, io=io)

        self.assertEqual(
            result,
            (program, 105, io),
        )

    def test_jump_if_false(self):
        program = [0, 6, 1, 2]
        io = IO()
        result = execute_next_instruction(program, pointer=1, io=io)

        self.assertEqual(
            result,
            (program, 4, io),
        )

        program = [0, 6, 0, 1]
        io = IO()
        result = execute_next_instruction(program, pointer=1, io=io)

        self.assertEqual(
            result,
            (program, 6, io),
        )

        program = [0, 106, 0, 1]
        io = IO()
        result = execute_next_instruction(program, pointer=1, io=io)

        self.assertEqual(
            result,
            (program, 106, io),
        )


    def test_less_than(self):
        program = [1, 7, 3, 2, 1]
        io = IO()
        result = execute_next_instruction(program, pointer=1, io=io)

        self.assertEqual(
            result,
            ([1, 1, 3, 2, 1], 5, io),
            (
                'if the first parameter (position mode) is less than the second parameter, '
                '(position mode) it stores 1 in the position given by the third parameter'
            )
        )

        program = [1, 1107, 2, 3, 1]
        io = IO()
        result = execute_next_instruction(program, pointer=1, io=io)

        self.assertEqual(
            result,
            ([1, 1, 2, 3, 1], 5, io),
            (
                'if the first parameter (immediate mode) is less than the second parameter, '
                '(immmediate mode) it stores 1 in the position given by the third parameter'
            )
        )

        program = [1, 7, 1, 2, 1]
        io = IO()
        result = execute_next_instruction(program, pointer=1, io=io)

        self.assertEqual(
            result,
            ([1, 0, 1, 2, 1], 5, io),
            (
                'if the first parameter (position mode) is >= the second parameter, '
                '(position mode) it stores 0 in the position given by the third parameter'
            )
        )

        program = [1, 1107, 2, 1, 1]
        io = IO()
        result = execute_next_instruction(program, pointer=1, io=io)

        self.assertEqual(
            result,
            ([1, 0, 2, 1, 1], 5, io),
            (
                'if the first parameter (immediate mode) is >= the second parameter, '
                '(immediate mode) it stores 0 in the position given by the third parameter'
            )
        )

    def test_equals(self):
        program = [1, 8, 0, 5, 1, 1]
        io = IO()
        result = execute_next_instruction(program, pointer=1, io=io)

        self.assertEqual(
            result,
            ([1, 1, 0, 5, 1, 1], 5, io),
            (
                'if the first parameter (position mode) is equal to the second parameter, '
                '(position mode) it stores 1 in the position given by the third parameter'
            )
        )

        program = [1, 1108, 5, 5, 1, 1]
        io = IO()
        result = execute_next_instruction(program, pointer=1, io=io)

        self.assertEqual(
            result,
            ([1, 1, 5, 5, 1, 1], 5, io),
            (
                'if the first parameter (immediate mode) is equal to the second parameter, '
                '(immediate mode) it stores 1 in the position given by the third parameter'
            )
        )

        program = [1, 8, 0, 5, 1, 2]
        io = IO()
        result = execute_next_instruction(program, pointer=1, io=io)

        self.assertEqual(
            result,
            ([1, 0, 0, 5, 1, 2], 5, io),
            (
                'if the first parameter (position mode) is not equal to the second parameter, '
                '(position mode) it stores 0 in the position given by the third parameter'
            )
        )

        program = [1, 1108, 5, 4, 1, 1]
        io = IO()
        result = execute_next_instruction(program, pointer=1, io=io)

        self.assertEqual(
            result,
            ([1, 0, 5, 4, 1, 1], 5, io),
            (
                'if the first parameter (immediate mode) is not equal to the second parameter, '
                '(immediate mode) it stores 0 in the position given by the third parameter'
            )
        )

    def test_execute(self):
        program = [1002,4,3,4,33]
        io = IO()
        result = execute(program, pointer=0, io=io)
        self.assertEqual(
            ([1002, 4, 3, 4, 99], None, io),
            result,
            'Execute the program'
        )

    def test_program_01(self):
        program = [3,9,8,9,10,9,4,9,99,-1,8]
        io = IO(initial_io={ 'input': ['8'], 'output': ['1'] })
        execute(program, pointer=0, io=io)

        self.assertEqual(
            io.get_next_output(),
            '1'
        )

    def test_connected_programs(self):
        program = [
            3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
            27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5
        ]
        initial_output = 0
        phase_setting = [9,8,7,6,5]
        result = execute_connected_programs(
            [
                Machine(program[:]),
                Machine(program[:]),
                Machine(program[:]),
                Machine(program[:]),
                Machine(program[:]),
            ],
            phase_setting,
            initial_output,
        )
        self.assertEqual(
            result,
            139629729
        )

if __name__ == '__main__':
    unittest.main()
