import csv


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

def add(program, pointer):
    param_num = 3
    mode_args = get_mode_args(program, pointer, param_num)

    addendum1 = read_value(program, mode_args[0])
    addendum2 = read_value(program, mode_args[1])
    (_, position) = mode_args[2]
    program_copy = program[:]
    program_copy[position] = addendum1 + addendum2
    return (program_copy, pointer_to_next_instruction(pointer, param_num))


def mul(program, pointer):
    param_num = 3
    mode_args = get_mode_args(program, pointer, param_num)

    factor1 = read_value(program, mode_args[0])
    factor2 = read_value(program, mode_args[1])
    (_, position) = mode_args[2]
    program_copy = program[:]
    program_copy[position] = factor1 * factor2
    return (program_copy, pointer_to_next_instruction(pointer,param_num))


def halt(program, pointer):
    program_copy = program[:]
    return (program_copy, None)


def store_input(program, pointer):
    param_num = 1

    program_copy = program[:]
    program_copy[program_copy[pointer + 1]] = int(input())
    return (program_copy, pointer_to_next_instruction(pointer, param_num))


def output(program, pointer):
    param_num = 1

    program_copy = program[:]
    print(program_copy[program_copy[pointer + 1]])
    return (program_copy, pointer_to_next_instruction(pointer,param_num))


def jump_if_true(program, pointer):
    param_num = 2
    mode_args = get_mode_args(program, pointer, param_num)
    condition = read_value(program, mode_args[0])
    if condition != 0:
        return (program, read_value(program, mode_args[1]))
    return (program, pointer_to_next_instruction(pointer, param_num))


def jump_if_false(program, pointer):
    param_num = 2
    mode_args = get_mode_args(program, pointer, param_num)
    condition = read_value(program, mode_args[0])
    if condition == 0:
        return (program, read_value(program, mode_args[1]))
    return (program, pointer_to_next_instruction(pointer, param_num))

def less_than(program, pointer):
    param_num = 3
    mode_args = get_mode_args(program, pointer, param_num)
    (_, _, store_to) = get_args(program, pointer, param_num)
    program_copy = program[:]

    if read_value(program, mode_args[0]) < read_value(program, mode_args[1]):
        program_copy[store_to] = 1
    else:
        program_copy[store_to] = 0
    return (program_copy, pointer_to_next_instruction(pointer, param_num))


def equals(program, pointer):
    param_num = 3
    mode_args = get_mode_args(program, pointer, param_num)
    (_, _, store_to) = get_args(program, pointer, param_num)
    program_copy = program[:]

    if read_value(program, mode_args[0]) == read_value(program, mode_args[1]):
        program_copy[store_to] = 1
    else:
        program_copy[store_to] = 0
    return (program_copy, pointer_to_next_instruction(pointer, param_num))



def execute_next_instruction(program, pointer):
    opcode = get_opcode(program[pointer])
    if opcode == 1:
        return add(program, pointer)
    if opcode == 2:
        return mul(program, pointer)
    if opcode == 99:
        return halt(program, pointer)
    if opcode == 3:
        return store_input(program, pointer)
    if opcode == 4:
        return output(program, pointer)
    if opcode == 5:
        return jump_if_true(program, pointer)
    if opcode == 6:
        return jump_if_false(program, pointer)
    if opcode == 7:
        return less_than(program, pointer)
    if opcode == 8:
        return equals(program, pointer)
    else:
        raise ValueError(f'Invalid opcode: {opcode}')


def execute(program, pointer=0):
      (resulted_program, next_pointer) = execute_next_instruction(program, pointer)
      if next_pointer == None:
          return resulted_program
      return execute(resulted_program, next_pointer)

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

if __name__ == '__main__':
    with open('./input.txt') as fiddle_input:
        [original_program] = csv.reader(fiddle_input, delimiter=',')
        original_program = [int(value) for value in original_program]
        program = original_program[:]
        execute(program)