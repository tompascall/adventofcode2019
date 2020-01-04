import csv


def get_opcode(token):
    return int(str(token)[-2:])

def get_modes(token, arg_num):
    filled_modes = str(token)[:-2].zfill(arg_num)
    reversed_modes = filled_modes[::-1]
    return [int(mode) for mode in reversed_modes]

def get_value(program, token):
    (mode, code) = token
    if mode == 0:
        return program[code]
    if mode == 1:
        return code
    else:
        raise f'Invalid mode: {mode}'


def add(program, pointer):
    length = 4
    modes = get_modes(program[pointer], 3)
    args = tuple(zip(modes, program[pointer + 1:pointer + 4]))

    addendum1 = get_value(program, args[0])
    addendum2 = get_value(program, args[1])
    (_, position) = args[2]
    program_copy = program[:]
    program_copy[position] = addendum1 + addendum2
    return (program_copy, pointer + length)


def mul(program, pointer):
    length = 4
    modes = get_modes(program[pointer], 3)
    args = tuple(zip(modes, program[pointer + 1:pointer + 4]))

    factor1 = get_value(program, args[0])
    factor2 = get_value(program, args[1])
    (_, position) = args[2]
    program_copy = program[:]
    program_copy[position] = factor1 * factor2
    return (program_copy, pointer + length)


def halt(program, pointer):
    program_copy = program[:]
    return (program_copy, None)


def store_input(program, pointer):
    length = 2

    program_copy = program[:]
    print('Your input: ')
    program_copy[program_copy[pointer + 1]] = int(input())
    return (program_copy, pointer + length)


def output(program, pointer):
    length = 2

    program_copy = program[:]
    print(program_copy[program_copy[pointer + 1]])
    return (program_copy, pointer + length)


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
    else:
        raise ValueError(f'Invalid opcode: {opcode}')


def execute(program, pointer=0):
      (resulted_program, next_pointer) = execute_next_instruction(program, pointer)
      if next_pointer == None:
          return resulted_program
      return execute(resulted_program, next_pointer)

if __name__ == '__main__':
    with open('./input.txt') as fiddle_input:
        [original_program] = csv.reader(fiddle_input, delimiter=',')
        original_program = [int(value) for value in original_program]
        program = original_program[:]
        execute(program)