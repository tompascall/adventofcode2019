import csv

def build_orbit_parents(map):
    orbit_parents = {}
    for [parent, obj] in map:
        orbit_parents[obj] = parent
    return orbit_parents

def count_parents(orbit_parents, orbit):
    parent = orbit_parents.get(orbit, None)
    if  parent == None:
        return 0
    return 1 + count_parents(orbit_parents, parent)

def get_checksum(map):
    orbit_parents = build_orbit_parents(map)
    checksum = 0
    for orbit in orbit_parents:
        checksum = checksum + count_parents(orbit_parents, orbit)
    return checksum

def get_parents(orbit_parents, orbit):
    parent = orbit_parents.get(orbit, None)
    if parent == None:
        return []
    return [parent] + get_parents(orbit_parents, parent)

def get_first_common_parent(orbit_parents, orb1, orb2):
    orb1_parents = get_parents(orbit_parents, orb1)
    orb2_parents = get_parents(orbit_parents, orb2)
    common_parents = [
        orb1_parent for orb1_parent in orb1_parents if orb1_parent in orb2_parents
    ]
    return common_parents[0]

def count_parents_to(orbit_parents, orbit, to):
    parent = orbit_parents.get(orbit, None)
    if  parent == None:
        raise ValueError(f'{orbit} does not have {to} parent')
    if parent == to:
        return 0
    return 1 + count_parents_to(orbit_parents, parent, to)

def count_min_transfers(map, orb1, orb2):
    orbit_parents = build_orbit_parents(map)
    first_common_parent = get_first_common_parent(orbit_parents, orb1, orb2)
    return (
        count_parents_to(orbit_parents, orb1, first_common_parent) +
        count_parents_to(orbit_parents, orb2, first_common_parent)
    )

if __name__ == '__main__':
    with open('./input.txt') as fiddle_input:
        map = [orbit_relation for orbit_relation in csv.reader(fiddle_input, delimiter=')')]
        print(get_checksum(map))
        print(count_min_transfers(map, 'YOU', 'SAN'))
