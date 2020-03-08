import itertools as it

def get_layers(digits, width, height):
    layer_num = int(len(digits) / (width * height))
    digits = (digit for digit in digits)

    def get_next_layer(digits, height, width):
        layer = [list(it.islice(digits, width)) for _ in range(height)]
        return layer

    layers = [get_next_layer(digits, height, width) for _ in range(layer_num)]
    return layers

def count_digit_in_layer(layer, digit):
    flatten_layer = list(it.chain.from_iterable(layer))
    return len([elem for elem in flatten_layer if elem == digit])

if __name__ == '__main__':
    with open('./input.txt') as fiddle_input:
        digits = fiddle_input.read()
        layers = get_layers(digits, 25, 6)
        zeronums = [count_digit_in_layer(layer, '0') for layer in layers]
        focused_layer = layers[zeronums.index(min(zeronums))]
        print(count_digit_in_layer(focused_layer, '1') * count_digit_in_layer(focused_layer, '2'))