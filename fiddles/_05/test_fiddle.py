from unittest.mock import patch
from io import StringIO
import unittest
from fiddles._05.fiddle import (
    execute_next_instruction,
    execute,
    mul,
    add,
    halt,
    store_input,
    output,
)


class TestFiddle(unittest.TestCase):
    def test_execute_next_instruction_mul(self):
        program = [0,1002,5,3,5,33]
        result = execute_next_instruction(program, pointer=1)

        self.assertEqual(
            result,
            ([0, 1002, 5, 3, 5, 99], 5)
        )

    def test_execute_next_instruction_add(self):
        program = [0,1001,5,3,5,33]
        result = execute_next_instruction(program, pointer=1)

        self.assertEqual(
            result,
            ([0, 1001, 5, 3, 5, 36], 5)
        )

    def test_execute_next_instruction_halt(self):
        program = [1001,4,3,4,99]
        result = execute_next_instruction(program, pointer=4)

        self.assertEqual(
            result,
            ([1001,4,3,4,99], None)
        )

    def test_execute_next_instruction_store_input(self):
        program = [0,3,2]

        mock_input = ['10']
        with patch('builtins.input', side_effect=mock_input):
            result = execute_next_instruction(program, pointer=1)

        self.assertEqual(
            result,
            ([0, 3, 10], 3)
        )

    def test_execute_next_instruction_output(self):
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

    def test_execute(self):
        program = [1002,4,3,4,33]
        result = execute(program)
        self.assertEqual(
            [1002, 4, 3, 4, 99],
            result,
            'Execute the program'
        )


if __name__ == '__main__':
    unittest.main()
