import itertools as it
import pprint

WHITE = '1'
BLACK = '0'

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

def merge_layers(layers, height):
    def get_rows_in_height(row_num):
        return [layer[row_num] for layer in layers]

    def merge_pixel(zipped_row):
        def get_pixel_value(pixel_in_layers):
            white_index = pixel_in_layers.index(WHITE) if WHITE in pixel_in_layers else -1
            black_index = pixel_in_layers.index(BLACK) if BLACK in pixel_in_layers else -1
            if white_index != -1 and white_index < black_index or black_index == -1:
                return WHITE
            return BLACK

        return [get_pixel_value(pixel_in_layers) for pixel_in_layers in zipped_row]

    zipped_rows = [list(zip(*get_rows_in_height(row_num))) for row_num in range(height)]
    return [merge_pixel(zipped_row) for zipped_row in zipped_rows]


if __name__ == '__main__':
    with open('./input.txt') as fiddle_input:
        digits = fiddle_input.read()
        height = 6
        width = 25
        layers = get_layers(digits, width, height)
        zeronums = [count_digit_in_layer(layer, '0') for layer in layers]
        focused_layer = layers[zeronums.index(min(zeronums))]
        print(count_digit_in_layer(focused_layer, '1') * count_digit_in_layer(focused_layer, '2'))
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint([''.join(row) for row in merge_layers(layers, height)])