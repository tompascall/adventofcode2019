import unittest
from fiddles._09.fiddle import (
    IO,
    Machine,
)


class TestFiddle(unittest.TestCase):
    def test_machine_mul(self):
        program = [1002,4,3,4,33]
        machine = Machine(program)
        machine.execute_next_instruction()
        self.assertEqual(
            machine.get_program(),
            [1002, 4, 3, 4, 99]
        )
        self.assertEqual(
            machine.get_pointer(),
            4
        )

    def test_machine_add(self):
        program = [0,1001,5,3,5,33]
        machine = Machine(program, 1)
        machine.execute_next_instruction()
        self.assertEqual(
            machine.get_program(),
            [0, 1001, 5, 3, 5, 36]
        )
        self.assertEqual(
            machine.get_pointer(),
            5
        )

    def test_machine_halt(self):
        program = [1001,4,3,4,99]
        machine = Machine(program, 4)
        machine.execute_next_instruction()
        self.assertEqual(
            machine.get_program(),
            [1001,4,3,4,99]
        )
        self.assertEqual(
            machine.get_pointer(),
            None
        )

    def test_machine_store_input(self):
        program = [0,3,2]
        io = IO(initial_io={ 'input': ['10'], 'output': [] })
        machine = Machine(program, 1, io)
        machine.execute_next_instruction()
        self.assertEqual(
            machine.get_program(),
            [0, 3, 10]
        )
        self.assertEqual(
            machine.get_pointer(),
            3
        )

    def test_machine_output(self):
        program = [0,4,3,50]
        machine = Machine(program, 1)
        machine.execute_next_instruction()
        self.assertEqual(
            machine.get_program(),
            [0,4,3,50]
        )
        self.assertEqual(
            machine.get_pointer(),
            3
        )
        self.assertEqual(
            machine.io.get_next_output(),
            '50'
        )

    def test_machine_jump_if_true(self):
        program = [0, 5, 0, 2]
        machine = Machine(program, 1)
        machine.execute_next_instruction()
        self.assertEqual(
            machine.get_program(),
            program
        )
        self.assertEqual(
            machine.get_pointer(),
            4
        )

        program = [0, 5, 1, 1]
        machine = Machine(program, 1)
        machine.execute_next_instruction()
        self.assertEqual(
            machine.get_program(),
            program
        )
        self.assertEqual(
            machine.get_pointer(),
            5
        )

        program = [0, 105, 1, 1]
        machine = Machine(program, 1)
        machine.execute_next_instruction()
        self.assertEqual(
            machine.get_program(),
            program
        )
        self.assertEqual(
            machine.get_pointer(),
            105
        )

    def test_machine_jump_if_false(self):
        program = [0, 6, 1, 2]
        machine = Machine(program, 1)
        machine.execute_next_instruction()
        self.assertEqual(
            machine.get_program(),
            program
        )
        self.assertEqual(
            machine.get_pointer(),
            4
        )

        program = [0, 6, 0, 1]
        machine = Machine(program, 1)
        machine.execute_next_instruction()
        self.assertEqual(
            machine.get_program(),
            program
        )
        self.assertEqual(
            machine.get_pointer(),
            6
        )

        program = [0, 106, 0, 1]
        machine = Machine(program, 1)
        machine.execute_next_instruction()
        self.assertEqual(
            machine.get_program(),
            program
        )
        self.assertEqual(
            machine.get_pointer(),
            106
        )

    def test_machine_less_than(self):
        program = [1, 7, 3, 2, 1]
        machine = Machine(program, 1)
        machine.execute_next_instruction()
        self.assertEqual(
            machine.get_program(),
            [1, 1, 3, 2, 1]
        )
        self.assertEqual(
            machine.get_pointer(),
            5,
            (
                'if the first parameter (position mode) is less than the second parameter, '
                '(position mode) it stores 1 in the position given by the third parameter'
            )
        )

        program = [1, 1107, 2, 3, 1]
        machine = Machine(program, 1)
        machine.execute_next_instruction()
        self.assertEqual(
            machine.get_program(),
            [1, 1, 2, 3, 1]
        )
        self.assertEqual(
            machine.get_pointer(),
            5,
            (
                'if the first parameter (immediate mode) is less than the second parameter, '
                '(immmediate mode) it stores 1 in the position given by the third parameter'
            )
        )

        program = [1, 7, 1, 2, 1]
        machine = Machine(program, 1)
        machine.execute_next_instruction()
        self.assertEqual(
            machine.get_program(),
            [1, 0, 1, 2, 1]
        )
        self.assertEqual(
            machine.get_pointer(),
            5,
            (
                'if the first parameter (position mode) is >= the second parameter, '
                '(position mode) it stores 0 in the position given by the third parameter'
            )
        )

        program = [1, 1107, 2, 1, 1]
        machine = Machine(program, 1)
        machine.execute_next_instruction()
        self.assertEqual(
            machine.get_program(),
            [1, 0, 2, 1, 1]
        )
        self.assertEqual(
            machine.get_pointer(),
            5,
            (
                'if the first parameter (immediate mode) is >= the second parameter, '
                '(immediate mode) it stores 0 in the position given by the third parameter'
            )
        )

    def test_machine_equals(self):
        program = [1, 8, 0, 5, 1, 1]
        machine = Machine(program, 1)
        machine.execute_next_instruction()
        self.assertEqual(
            machine.get_program(),
            [1, 1, 0, 5, 1, 1]
        )
        self.assertEqual(
            machine.get_pointer(),
            5,
            (
                'if the first parameter (position mode) is equal to the second parameter, '
                '(position mode) it stores 1 in the position given by the third parameter'
            )
        )

        program = [1, 1108, 5, 5, 1, 1]
        machine = Machine(program, 1)
        machine.execute_next_instruction()
        self.assertEqual(
            machine.get_program(),
            [1, 1, 5, 5, 1, 1]
        )
        self.assertEqual(
            machine.get_pointer(),
            5,
            (
                'if the first parameter (immediate mode) is equal to the second parameter, '
                '(immediate mode) it stores 1 in the position given by the third parameter'
            )
        )

        program = [1, 8, 0, 5, 1, 2]
        machine = Machine(program, 1)
        machine.execute_next_instruction()
        self.assertEqual(
            machine.get_program(),
            [1, 0, 0, 5, 1, 2]
        )
        self.assertEqual(
            machine.get_pointer(),
            5,
            (
                'if the first parameter (position mode) is not equal to the second parameter, '
                '(position mode) it stores 0 in the position given by the third parameter'
            )
        )

        program = [1, 1108, 5, 4, 1, 1]
        machine = Machine(program, 1)
        machine.execute_next_instruction()
        self.assertEqual(
            machine.get_program(),
            [1, 0, 5, 4, 1, 1]
        )
        self.assertEqual(
            machine.get_pointer(),
            5,
            (
                'if the first parameter (immediate mode) is not equal to the second parameter, '
                '(immediate mode) it stores 0 in the position given by the third parameter'
            )
        )

    def test_machine_run(self):
        program = [1002,4,3,4,33]
        machine = Machine(program, 0)
        machine.run()
        self.assertEqual(
            machine.get_program(),
            [1002, 4, 3, 4, 99]
        )
        self.assertEqual(
            machine.get_pointer(),
            None
        )

    def test_program_01(self):
        program = [3,9,8,9,10,9,4,9,99,-1,8]
        io = IO(initial_io={ 'input': ['8'], 'output': ['1'] })
        machine = Machine(program, 0, io)
        machine.run()

        self.assertEqual(
            machine.io.get_next_output(),
            '1'
        )

if __name__ == '__main__':
    unittest.main()
