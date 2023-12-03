SYMBOLS = ['*', '@', '-', '+', '#', '%', '=', '/', '$', '&']
INPUT_LINE_LENGTH = 140
INPUT_LIST_LENGTH = 140


def setup() -> list[str]:
    file = open("engine_parts.txt", "r")
    data = file.readlines()
    file.close()
    return data


def provide_x_range(x_end, element_length) -> [int]:
    x_min = x_end - element_length - 1
    x_min = 0 if x_min < 0 else x_min
    x_max = x_end + 1
    x_max = INPUT_LINE_LENGTH if x_max > INPUT_LINE_LENGTH else x_max
    return range(x_min, x_max)


def provide_y_range(y) -> [int]:
    y_min = y - 1
    y_min = 0 if y_min < 0 else y_min
    y_max = y + 1
    y_max = INPUT_LIST_LENGTH if y_max > INPUT_LIST_LENGTH else y_max
    return range(y_min, y_max + 1)


def compose_spot(x_end, y, element) -> [tuple]:
    spot = []
    for y in provide_y_range(y):
        for x in provide_x_range(x_end, len(element)):
            if x < 0 or y < 0:
                continue
            spot.append((x, y))

    return spot


def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))


def index_symbols(lines: list[str]) -> tuple:
    numbers_map = []
    symbols_map = []
    asterix_map = []
    y = 0
    for line in lines:
        element = ""
        x = 0
        for char in line:
            is_symbol = char in SYMBOLS
            is_asterix = char == "*"
            if is_symbol:
                symbols_map.append((x, y))
                if is_asterix:
                    asterix_map.append((x, y))

            if (char == "." or char == "\n" or is_symbol) and element != "":
                numbers_map.append(
                    {"number": int(element),
                     "spot": compose_spot(x, y, element)})
                element = ""

            if char.isdigit():
                element += char
            x += 1
        y += 1

    return numbers_map, symbols_map, asterix_map


def find_engine_parts(n_map: dict, s_map: list) -> [int]:
    return [number_map for number_map in n_map if intersection(number_map.get("spot"), s_map)]


def find_gears(parts_map: dict, asterix_map: list) -> [int]:
    gears = []
    for asterix_xy in asterix_map:
        parts = [part.get("number") for part in parts_map if asterix_xy in part.get("spot")]
        if len(parts) > 1:
            gears.append(parts)
    return gears


if __name__ == '__main__':
    input_strings = setup()
    numbers_map, symbols_map, asterix_map = index_symbols(input_strings)
    engine_parts = find_engine_parts(numbers_map, symbols_map)
    gears = find_gears(engine_parts, asterix_map)
    print(sum([part.get("number") for part in engine_parts]))
    print(sum([part1 * part2 for part1, part2 in gears]))
