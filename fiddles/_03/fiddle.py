import csv
import re

def get_route(origo, token):
    splitted_token = re.search('([LRUD])([0-9]+)', token)
    (origo_x, origo_y) = origo
    direction = splitted_token.group(1)
    length = int(splitted_token.group(2))
    if direction == 'R':
        return [(origo_x + step, origo_y) for step in range(1, length +  1)]
    if direction == 'L':
        return [(origo_x - step, origo_y) for step in range(1, length +  1)]
    if direction == 'U':
        return [(origo_x, origo_y + step) for step in range(1, length +  1)]
    if direction == 'D':
        return [(origo_x, origo_y - step) for step in range(1, length +  1)]

def tokens_to_coords(tokens, origo):
    coords = [origo]
    for token in tokens:
        route = get_route(origo, token)
        coords += route
        origo = route[-1]
    return coords


if __name__ == '__main__':
    with open('./input.txt') as fiddle_input:
        wires = [tokens_to_coords(wire, (0, 0))
           for wire in csv.reader(fiddle_input.readlines(), delimiter=',')]
        crosses = list(set(wires[0]).intersection(set(wires[1])))
        print(
            sorted(crosses, key=lambda koord: abs(koord[0]) + abs(koord[1]))[1],
            min([wires[0].index(cross) + wires[1].index(cross)
                for cross in crosses if cross != (0, 0)
            ])
        )