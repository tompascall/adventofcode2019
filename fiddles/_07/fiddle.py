import csv
from functional import compose
import functools


class State:
    def __init__(self, initial_state={ 'input': [], 'output': [] }):
        self.input = initial_state['input']
        self.output = initial_state['output']

    def get_next_input(self):
        return self.input.pop()

    def get_next_output(self):
        return self.output.pop()

    def store_input(self, i):
        self.input = [i] + self.input
        # print('storing input', i, 'input=', self.input, 'output=', self.output)

    def store_output(self, o):
        self.output = [o] + self.output
        # print('storing output', o, 'input=', self.input, 'output=', self.output)

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

def add(program, pointer, state):
    param_num = 3
    mode_args = get_mode_args(program, pointer, param_num)

    addendum1 = read_value(program, mode_args[0])
    addendum2 = read_value(program, mode_args[1])
    (_, position) = mode_args[2]
    program_copy = program[:]
    program_copy[position] = addendum1 + addendum2
    return (program_copy, pointer_to_next_instruction(pointer, param_num), state)


def mul(program, pointer, state):
    param_num = 3
    mode_args = get_mode_args(program, pointer, param_num)

    factor1 = read_value(program, mode_args[0])
    factor2 = read_value(program, mode_args[1])
    (_, position) = mode_args[2]
    program_copy = program[:]
    program_copy[position] = factor1 * factor2
    return (program_copy, pointer_to_next_instruction(pointer,param_num), state)


def halt(program, pointer, state):
    program_copy = program[:]
    return (program_copy, None, state)


def store_input(program, pointer, state):
    param_num = 1

    program_copy = program[:]
    program_copy[program_copy[pointer + 1]] = int(state.get_next_input())
    return (program_copy, pointer_to_next_instruction(pointer, param_num), state)


def output(program, pointer, state):
    param_num = 1

    program_copy = program[:]
    output = program_copy[program_copy[pointer + 1]]
    state.store_output(str(output))
    return (program_copy, pointer_to_next_instruction(pointer,param_num), state)


def jump_if_true(program, pointer, state):
    param_num = 2
    mode_args = get_mode_args(program, pointer, param_num)
    condition = read_value(program, mode_args[0])
    if condition != 0:
        return (program, read_value(program, mode_args[1]), state)
    return (program, pointer_to_next_instruction(pointer, param_num), state)


def jump_if_false(program, pointer, state):
    param_num = 2
    mode_args = get_mode_args(program, pointer, param_num)
    condition = read_value(program, mode_args[0])
    if condition == 0:
        return (program, read_value(program, mode_args[1]), state)
    return (program, pointer_to_next_instruction(pointer, param_num), state)

def less_than(program, pointer, state):
    param_num = 3
    mode_args = get_mode_args(program, pointer, param_num)
    (_, _, store_to) = get_args(program, pointer, param_num)
    program_copy = program[:]

    if read_value(program, mode_args[0]) < read_value(program, mode_args[1]):
        program_copy[store_to] = 1
    else:
        program_copy[store_to] = 0
    return (program_copy, pointer_to_next_instruction(pointer, param_num), state)


def equals(program, pointer, state):
    param_num = 3
    mode_args = get_mode_args(program, pointer, param_num)
    (_, _, store_to) = get_args(program, pointer, param_num)
    program_copy = program[:]

    if read_value(program, mode_args[0]) == read_value(program, mode_args[1]):
        program_copy[store_to] = 1
    else:
        program_copy[store_to] = 0
    return (program_copy, pointer_to_next_instruction(pointer, param_num), state)



def execute_next_instruction(program, pointer, state):
    opcode = get_opcode(program[pointer])
    if opcode == 1:
        return add(program, pointer, state)
    if opcode == 2:
        return mul(program, pointer, state)
    if opcode == 99:
        return halt(program, pointer, state)
    if opcode == 3:
        return store_input(program, pointer, state)
    if opcode == 4:
        return output(program, pointer, state)
    if opcode == 5:
        return jump_if_true(program, pointer, state)
    if opcode == 6:
        return jump_if_false(program, pointer, state)
    if opcode == 7:
        return less_than(program, pointer, state)
    if opcode == 8:
        return equals(program, pointer, state)
    else:
        print('before error' , state.input, state.output)
        raise ValueError(f'Invalid opcode: {opcode}')


def execute(program, pointer=0, state=None):
      (resulted_program, next_pointer, state) = execute_next_instruction(program, pointer, state)
      if next_pointer == None:
          return (resulted_program, None, state)
      return execute(resulted_program, next_pointer, state)

def swap(pairs):
    [first, second] = pairs
    return [second, first]

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

def amplifier_executer(amplifier, phase_setting):
    def executer(initial_input):
        (_, _, state) = initial_input
        output = state.get_next_output()
        state.store_input(phase_setting)
        state.store_input(output)
        return execute(amplifier, 0, state)
    return executer


if __name__ == '__main__':
    with open('./input.txt') as fiddle_input:
        [original_program] = csv.reader(fiddle_input, delimiter=',')
        original_program = [int(value) for value in original_program]
        amplifiers = [
            original_program[:],
            original_program[:],
            original_program[:],
            original_program[:],
            original_program[:]
        ]
        phase_settings = permutations([0,1,2,3,4])
        thruster_signals = []

        for phase_setting in phase_settings:
            state = State(initial_state={ 'input': [], 'output': [0] })
            amplifier_executer(amplifiers[4], phase_setting[4])(
                amplifier_executer(amplifiers[3], phase_setting[3])(
                    amplifier_executer(amplifiers[2], phase_setting[2])(
                        amplifier_executer(amplifiers[1], phase_setting[1])(
                            amplifier_executer(amplifiers[0], phase_setting[0])((None, None, state))
                        )
                    )
                )
            )

            thruster_signals.append(state.get_next_output())

        print(max(thruster_signals))