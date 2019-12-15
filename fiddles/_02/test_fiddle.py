import unittest
from fiddles._02.fiddle import (
    replace_code,
    execute_instruction,
    get_instructions,
    set_noun,
    set_verb,
)


class TestFiddle(unittest.TestCase):
    def test_replace_code(self):
        test_data = [1, 2, 3]
        replaced = replace_code(test_data, position=0, new_value=4)
        self.assertEqual([4, 2, 3], replaced, 'Replace pos 0 to 4')

    def set_noun(self):
        program = [1, 2, 3]
        self.assertEqual(set_noun(program, 12), [1, 12, 3],
        'Set noun (1st pos)'
    )

    def set_verb(self):
        program = [1, 2, 3]
        self.assertEqual(set_noun(program, 12), [1, 2, 12],
        'Set verb (1st pos)'
    )

    def test_execute_instruction_exit(self):
        program = [99]
        instruction = (99,)
        self.assertEqual(program,
            execute_instruction(program, instruction),
            'Exit code'
        )

    def test_execute_instruction_add(self):
        program = [1, 2, 3, 4]
        instruction = (1, 0, 1, 3)
        self.assertEqual(
            [1, 2, 3, 3],
            execute_instruction(program, instruction),
            'Add pos 0 and pos 1 and save result to pos 3'
        )

    def test_execute_instruction_mul(self):
        program = [1, 2, 3, 4]
        instruction = (2, 1, 2, 3)
        self.assertEqual(
            [1, 2, 3, 6],
            execute_instruction(program, instruction),
            'Mul pos 1 and pos 2 and save resut to pos 3'
        )

    def test_get_instructions(self):
        program = [1,9,10,3,2,3,11,0,99,30,40,50]
        self.assertEqual(
            [
                (1,9,10,3),
                (2,3,11,0),
                (99,)
            ],
            get_instructions(program),
            'Get isntructions'
        )


if __name__ == '__main__':
    unittest.main()
