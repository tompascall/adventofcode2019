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

def pull_elem(elems, index):
    elems_copy = elems[::]
    elem = elems_copy.pop(index)
    return [
        elem,
        elems_copy
    ]

def create_node(elem, parent, child=None):
    return {
        'elem': elem,
        'parent': parent,
        'child': child
    }

def get_permutation(node):
    result = [node['elem']]
    while node['parent']['parent']:
        result.append(node['parent']['elem'])
        node = node['parent']
    return result

def get_permutations(elems, root, result):
    for index in range(len(elems)):
        [elem, rest] = pull_elem(elems, index)
        node = create_node(elem=elem, parent=root)
        if len(rest) > 0:
            node['child'] = get_permutations(rest, node, result)
        else:
            result.append(get_permutation(node))
    return result

def permutations(elems):
    return get_permutations(elems, root={ 'parent': None }, result=[])

def get_opcode(token):
    return int(str(token)[-2:])

def get_modes(program, pointer, param_num):
    filled_modes = str(program[pointer])[:-2].zfill(param_num)
    reversed_modes = filled_modes[::-1]
    return [int(mode) for mode in reversed_modes]

def read_value(program, mode_arg):
    (mode, arg) = mode_arg
    if mode == 0:
        return program[arg]
    if mode == 1:
        return arg
    else:
        raise f'Invalid mode: {mode}'

def get_args(program, pointer, param_num):
    return program[pointer + 1:pointer + param_num + 1]


def get_mode_args(program, pointer, param_num):
    modes = get_modes(program, pointer, param_num)
    args = get_args(program, pointer, param_num)
    return tuple(zip(modes, args))

def pointer_to_next_instruction(pointer, param_num):
    return pointer + param_num + 1

def add(program, pointer, io):
    param_num = 3
    mode_args = get_mode_args(program, pointer, param_num)

    addendum1 = read_value(program, mode_args[0])
    addendum2 = read_value(program, mode_args[1])
    (_, position) = mode_args[2]
    program_copy = program[:]
    program_copy[position] = addendum1 + addendum2
    return (program_copy, pointer_to_next_instruction(pointer, param_num), io)

def mul(program, pointer, io):
    param_num = 3
    mode_args = get_mode_args(program, pointer, param_num)

    factor1 = read_value(program, mode_args[0])
    factor2 = read_value(program, mode_args[1])
    (_, position) = mode_args[2]
    program_copy = program[:]
    program_copy[position] = factor1 * factor2
    return (program_copy, pointer_to_next_instruction(pointer,param_num), io)

def halt(program, pointer, io):
    program_copy = program[:]
    return (program_copy, None, io)

def store_input(program, pointer, io):
    param_num = 1

    program_copy = program[:]
    program_copy[program_copy[pointer + 1]] = int(io.get_next_input())
    return (program_copy, pointer_to_next_instruction(pointer, param_num), io)

def output(program, pointer, io):
    param_num = 1

    program_copy = program[:]
    output = program_copy[program_copy[pointer + 1]]
    io.store_output(str(output))
    return (program_copy, pointer_to_next_instruction(pointer,param_num), io)

def jump_if_true(program, pointer, io):
    param_num = 2
    mode_args = get_mode_args(program, pointer, param_num)
    condition = read_value(program, mode_args[0])
    if condition != 0:
        return (program, read_value(program, mode_args[1]), io)
    return (program, pointer_to_next_instruction(pointer, param_num), io)

def jump_if_false(program, pointer, io):
    param_num = 2
    mode_args = get_mode_args(program, pointer, param_num)
    condition = read_value(program, mode_args[0])
    if condition == 0:
        return (program, read_value(program, mode_args[1]), io)
    return (program, pointer_to_next_instruction(pointer, param_num), io)

def less_than(program, pointer, io):
    param_num = 3
    mode_args = get_mode_args(program, pointer, param_num)
    (_, _, store_to) = get_args(program, pointer, param_num)
    program_copy = program[:]

    if read_value(program, mode_args[0]) < read_value(program, mode_args[1]):
        program_copy[store_to] = 1
    else:
        program_copy[store_to] = 0
    return (program_copy, pointer_to_next_instruction(pointer, param_num), io)

def equals(program, pointer, io):
    param_num = 3
    mode_args = get_mode_args(program, pointer, param_num)
    (_, _, store_to) = get_args(program, pointer, param_num)
    program_copy = program[:]

    if read_value(program, mode_args[0]) == read_value(program, mode_args[1]):
        program_copy[store_to] = 1
    else:
        program_copy[store_to] = 0
    return (program_copy, pointer_to_next_instruction(pointer, param_num), io)

def execute_next_instruction(program, pointer, io):
    opcode = get_opcode(program[pointer])
    if opcode == 1:
        return add(program, pointer, io)
    if opcode == 2:
        return mul(program, pointer, io)
    if opcode == 99:
        return halt(program, pointer, io)
    if opcode == 3:
        return store_input(program, pointer, io)
    if opcode == 4:
        return output(program, pointer, io)
    if opcode == 5:
        return jump_if_true(program, pointer, io)
    if opcode == 6:
        return jump_if_false(program, pointer, io)
    if opcode == 7:
        return less_than(program, pointer, io)
    if opcode == 8:
        return equals(program, pointer, io)
    else:
        raise ValueError(f'Invalid opcode: {opcode}')

def execute(program, pointer=0, io=None):
      (resulted_program, next_pointer, io) = execute_next_instruction(program, pointer, io)
      if next_pointer == None or len(io.output):
          return (resulted_program, next_pointer, io)
      return execute(resulted_program, next_pointer, io)


class Machine():
    def __init__(self, program):
        self.program = program
        self.pointer = 0

    def get_program(self):
        return self.program

    def get_pointer(self):
        return self.pointer

    def run(self, io):
        (next_program, next_pointer, io) = execute(self.program, self.pointer, io)
        self.program = next_program
        self.pointer = next_pointer


def amplifier_executer(amplifier, io):
    output = io.get_next_output()
    if output != None:
        io.store_input(output)
    amplifier.run(io)

def execute_connected_programs(machines, phase_setting, initial_output):
    io = IO(initial_io={ 'input': [], 'output': [initial_output] })
    loop = 0
    while len(io.output):
        loop += 1
        for index in range(len(machines)):
            if loop == 1:
                io.store_input(phase_setting[index])
            amplifier_executer(machines[index], io)
    return int(io.input[0])

if __name__ == '__main__':
    with open('./input.txt') as fiddle_input:
        [original_program] = csv.reader(fiddle_input, delimiter=',')
        original_program = [int(value) for value in original_program]
        phase_settings = permutations([9,8,7,6,5])
        thruster_signals = []

        for phase_setting in phase_settings:
            amplifiers = [
                Machine(original_program[:]),
                Machine(original_program[:]),
                Machine(original_program[:]),
                Machine(original_program[:]),
                Machine(original_program[:])
            ]
            out = execute_connected_programs(amplifiers, phase_setting, 0)
            thruster_signals.append(out)

        print(max(thruster_signals))