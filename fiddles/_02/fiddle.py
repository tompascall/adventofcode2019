import csv

def replace_code(program, position, new_value):
    before = program[:position]
    after = program[position + 1:]
    return before + [new_value] + after

def set_noun(program, noun):
    return program[:1] + [noun] + program[2:]

def set_verb(program, verb):
    return program[:2] + [verb] + program[3:]

def add(program, instruction):
    (_, pos1, pos2, pos3) = instruction
    addendum1 = program[pos1]
    addendum2 = program[pos2]
    program_copy = program[:]
    program_copy[pos3] = addendum1 + addendum2
    return program_copy

def mul(program, instruction):
    (_, pos1, pos2, pos3) = instruction
    factor1 = program[pos1]
    factor2 = program[pos2]
    program_copy = program[:]
    program_copy[pos3] = factor1 * factor2
    return program_copy

def execute_instruction(program, instruction):
    opcode = instruction[0]
    if opcode == 99:
        return program
    elif opcode == 1:
        return add(program, instruction)
    elif opcode == 2:
        return mul(program, instruction)
    else:
        raise f'Invalid opcode: {opcode}'

def get_instructions(program):
    if program[0] == 99:
        return [(99,)]
    else:
        return [tuple(program[:4]), *get_instructions(program[4:])]


if __name__ == '__main__':
    with open('./input.txt') as fiddle_input:
        [original_program] = csv.reader(fiddle_input, delimiter=',')
        original_program = [int(value) for value in original_program]
        output = 19690720
        for noun in range(100):
            for verb in range(100):
                program = original_program[:]
                program = set_noun(program, noun)
                program = set_verb(program, verb)
                for instruction in get_instructions(program):
                    program = execute_instruction(program, instruction)
                if program[0] == output:
                    print(100 * noun + verb)
                    break
            if program[0] == output:
                break