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
    def __init__(self, program, pointer=0, io=None, relative_base=0, memory=0):
        self.program = program[:] + [0] * memory
        self.pointer = pointer or 0
        self.relative_base = relative_base or 0
        self.io = io or IO()
        self.memory = memory

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
        if mode == 2: # relative mode
            return self.program[arg + self.relative_base]
        else:
            raise f'Invalid mode: {mode}'

    def write_value(self, value, mode_arg):
        (mode, arg) = mode_arg
        if mode == 0: # position mode
            self.program[arg] = value
            return
        if mode == 2: # relative mode
            self.program[arg + self.relative_base] = value
            return
        else:
            raise f'Invalid mode: {mode}'

    def set_relative_base(self, mode_arg):
        (mode, arg) = mode_arg
        if mode == 0: # position mode
            self.relative_base += self.program[arg]
            return
        if mode == 1: # immediate mode
            self.relative_base += arg
            return
        if mode == 2: # relative mode
            self.relative_base += self.program[arg + self.relative_base]
            return
        else:
            raise f'Invalid mode: {mode}'

    def get_args(self, param_num):
        return self.program[self.pointer + 1:self.pointer + param_num + 1]

    def get_mode_args(self, param_num):
        modes = self.get_modes(param_num)
        args = self.get_args(param_num)
        return tuple(zip(modes, args))

    def pointer_to_next_instruction(self, param_num):
        print('.', end='')
        return self.pointer + param_num + 1

    def add(self):
        param_num = 3
        mode_args = self.get_mode_args(param_num)
        addendum1 = self.read_value(mode_args[0])
        addendum2 = self.read_value(mode_args[1])
        self.write_value(addendum1 + addendum2, mode_args[2])
        self.pointer = self.pointer_to_next_instruction(param_num)

    def mul(self):
        param_num = 3
        mode_args = self.get_mode_args(param_num)
        factor1 = self.read_value(mode_args[0])
        factor2 = self.read_value(mode_args[1])
        self.write_value(factor1 * factor2, mode_args[2])
        self.pointer = self.pointer_to_next_instruction(param_num)

    def halt(self):
        self.pointer = None

    def store_input(self):
        param_num = 1
        mode_args = self.get_mode_args(param_num)
        self.write_value(int(self.io.get_next_input()), mode_args[0])
        self.pointer = self.pointer_to_next_instruction(param_num)

    def output(self):
        param_num = 1
        program_copy = self.program[:]
        mode_args = self.get_mode_args(param_num)
        output = self.read_value(mode_args[0])
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

        if self.read_value(mode_args[0]) < self.read_value(mode_args[1]):
            self.write_value(1, mode_args[2])
        else:
            self.write_value(0, mode_args[2])
        self.pointer = self.pointer_to_next_instruction(param_num)

    def equals(self):
        param_num = 3
        mode_args = self.get_mode_args(param_num)

        if self.read_value(mode_args[0]) == self.read_value(mode_args[1]):
            self.write_value(1, mode_args[2])
        else:
            self.write_value(0, mode_args[2])
        self.pointer = self.pointer_to_next_instruction(param_num)

    def adjust_relative_base(self):
        param_num = 1
        mode_args = self.get_mode_args(param_num)
        self.set_relative_base(mode_args[0])
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
        elif opcode == 9:
            self.adjust_relative_base()
        else:
            raise ValueError(f'Invalid opcode: {opcode}')

    def run(self):
        while self.pointer != None:
            self.execute_next_instruction()


if __name__ == '__main__':
    with open('./input.txt') as fiddle_input:
        [original_program] = csv.reader(fiddle_input, delimiter=',')
        original_program = [int(value) for value in original_program]

        io = IO(initial_io={ 'input': ['2'], 'output': [] })
        machine = Machine(original_program, io=io, memory=2000)
        machine.run()
        print(machine.io.output)