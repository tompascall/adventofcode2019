import csv

def build_orbit_parents(input):
    orbit_parents = {}
    for [parent, obj] in input:
        orbit_parents[obj] = parent
    return orbit_parents

def count_parents(orbit_parents, orbit):
    parent = orbit_parents.get(orbit, None)
    if  parent == None:
        return 0
    return 1 + count_parents(orbit_parents, parent)

def get_checksum(input):
    orbit_parents = build_orbit_parents(input)
    checksum = 0
    for orbit in orbit_parents:
        checksum = checksum + count_parents(orbit_parents, orbit)
    return checksum


if __name__ == '__main__':
    with open('./input.txt') as fiddle_input:
        map = [input for input in csv.reader(fiddle_input, delimiter=')')]
        print(get_checksum(map))
