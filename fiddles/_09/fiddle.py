import csv

class IO:
    def __init__(self, initial_io={ 'input': [], 'output': [] }):
        self.input = initial_io['input']
        self.output = initial_io['output']

    def get_next_input(self):
        return self.input.pop()

    def get_next_output(self):
        if  len(self.output):
            return self.output.pop()
        return None

    def store_input(self, i):
        self.input = [i] + self.input

    def store_output(self, o):
        self.output = [o] + self.output


class Machine():
    def __init__(self, program, pointer=None, io=None):
        self.program = program
        self.pointer = pointer or 0
        self.io = io or IO()

    def get_program(self):
        return self.program

    def get_pointer(self):
        return self.pointer

    def get_opcode(self):
        token = self.program[self.pointer]
        return int(str(token)[-2:])

    def get_modes(self, param_num):
        filled_modes = str(self.program[self.pointer])[:-2].zfill(param_num)
        reversed_modes = filled_modes[::-1]
        return [int(mode) for mode in reversed_modes]

    def read_value(self, mode_arg):
        (mode, arg) = mode_arg
        if mode == 0: # position mode
            return self.program[arg]
        if mode == 1: # immediate mode
            return arg
        else:
            raise f'Invalid mode: {mode}'

    def get_args(self, param_num):
        return self.program[self.pointer + 1:self.pointer + param_num + 1]

    def get_mode_args(self, param_num):
        modes = self.get_modes(param_num)
        args = self.get_args(param_num)
        return tuple(zip(modes, args))

    def pointer_to_next_instruction(self, param_num):
        return self.pointer + param_num + 1

    def add(self):
        param_num = 3
        mode_args = self.get_mode_args(param_num)
        addendum1 = self.read_value(mode_args[0])
        addendum2 = self.read_value(mode_args[1])
        (_, position) = mode_args[2]
        program_copy = self.program[:]
        program_copy[position] = addendum1 + addendum2
        self.program = program_copy
        self.pointer = self.pointer_to_next_instruction(param_num)

    def mul(self):
        param_num = 3
        mode_args = self.get_mode_args(param_num)
        factor1 = self.read_value(mode_args[0])
        factor2 = self.read_value(mode_args[1])
        (_, position) = mode_args[2]
        program_copy = self.program[:]
        program_copy[position] = factor1 * factor2
        self.program = program_copy
        self.pointer = self.pointer_to_next_instruction(param_num)

    def halt(self):
        self.pointer = None

    def store_input(self):
        param_num = 1
        program_copy = self.program[:]
        program_copy[program_copy[self.pointer + 1]] = int(self.io.get_next_input())
        self.program = program_copy
        self.pointer = self.pointer_to_next_instruction(param_num)

    def output(self):
        param_num = 1
        program_copy = self.program[:]
        output = program_copy[program_copy[self.pointer + 1]]
        self.io.store_output(str(output))
        self.program = program_copy
        self.pointer = self.pointer_to_next_instruction(param_num)

    def jump_if_true(self):
        param_num = 2
        mode_args = self.get_mode_args(param_num)
        condition = self.read_value(mode_args[0])
        if condition != 0:
            self.pointer = self.read_value(mode_args[1])
        else:
            self.pointer = self.pointer_to_next_instruction(param_num)

    def jump_if_false(self):
        param_num = 2
        mode_args = self.get_mode_args(param_num)
        condition = self.read_value(mode_args[0])
        if condition == 0:
            self.pointer = self.read_value(mode_args[1])
        else:
            self.pointer = self.pointer_to_next_instruction(param_num)

    def less_than(self):
        param_num = 3
        mode_args = self.get_mode_args(param_num)
        (_, _, store_to) = self.get_args(param_num)
        program_copy = self.program[:]

        if self.read_value(mode_args[0]) < self.read_value(mode_args[1]):
            program_copy[store_to] = 1
        else:
            program_copy[store_to] = 0
        self.program = program_copy
        self.pointer = self.pointer_to_next_instruction(param_num)

    def equals(self):
        param_num = 3
        mode_args = self.get_mode_args(param_num)
        (_, _, store_to) = self.get_args(param_num)
        program_copy = self.program[:]

        if self.read_value(mode_args[0]) == self.read_value(mode_args[1]):
            program_copy[store_to] = 1
        else:
            program_copy[store_to] = 0
        self.program = program_copy
        self.pointer = self.pointer_to_next_instruction(param_num)

    def execute_next_instruction(self):
        opcode = self.get_opcode()
        if opcode == 1:
            self.add()
        elif opcode == 2:
            self.mul()
        elif opcode == 99:
            self.halt()
        elif opcode == 3:
            self.store_input()
        elif opcode == 4:
            self.output()
        elif opcode == 5:
            self.jump_if_true()
        elif opcode == 6:
            self.jump_if_false()
        elif opcode == 7:
            self.less_than()
        elif opcode == 8:
            self.equals()
        else:
            raise ValueError(f'Invalid opcode: {opcode}')

    def run(self):
        while self.pointer != None:
            self.execute_next_instruction()


if __name__ == '__main__':
    with open('./input.txt') as fiddle_input:
        [original_program] = csv.reader(fiddle_input, delimiter=',')
        original_program = [int(value) for value in original_program]
        # Machine(original_program[:])
