UNIVERSE_MAP: [str] = []
UNIVERSE_EXPANSION = 1000000


def is_column_empty(x) -> bool:
    for y, _ in enumerate(UNIVERSE_MAP):
        if UNIVERSE_MAP[y][x] == "#":
            return False
    return True


def is_row_empty(s: str) -> bool:
    return "#" not in s


def add_expansion_column(x) -> None:
    for y in range(len(UNIVERSE_MAP)):
        UNIVERSE_MAP[y] = f"{UNIVERSE_MAP[y][:x]}e{UNIVERSE_MAP[y][x + 1:]}"


def setup():
    file = open('universe.txt', 'r')
    lines = file.readlines()
    return [line.strip() for line in lines]


def build_map():
    lines = setup()
    for y, line in enumerate(lines):
        if is_row_empty(line):
            expansion_line = line[:].replace(".", "e")
            UNIVERSE_MAP.append(expansion_line)
        else:
            UNIVERSE_MAP.append(line)

    for x in range(len(lines[0])):
        col = ""
        for y in range(len(lines)):
            col += lines[y][x]
        if "#" not in col:
            add_expansion_column(x)


def find_galaxies():
    return {f"{y}_{x}": (y, x) for y, line in enumerate(UNIVERSE_MAP) for x, node in enumerate(line) if node == "#"}


def find_y_distance(x, from_d, to_d):
    dist = 0
    for y in range(min(from_d, to_d), max(from_d, to_d)):
        if UNIVERSE_MAP[y][x] == "e":
            dist += UNIVERSE_EXPANSION
        else:
            dist += 1
    return dist


def find_x_distance(y, from_d, to_d):
    dist = 0
    for x in range(min(from_d, to_d), max(from_d, to_d)):
        if UNIVERSE_MAP[y][x] == "e":
            dist += UNIVERSE_EXPANSION
        else:
            dist += 1
    return dist


def main():
    build_map()
    galaxies = find_galaxies()
    galaxy_distances = {}
    for galaxy_from in galaxies.keys():
        for galaxy_to in galaxies.keys():
            if galaxy_from == galaxy_to:
                continue
            key = tuple(sorted([galaxy_from, galaxy_to]))
            if key in galaxy_distances:
                continue
            y_dist = find_y_distance(galaxies[galaxy_from][1], galaxies[galaxy_from][0], galaxies[galaxy_to][0])
            x_dist = find_x_distance(galaxies[galaxy_from][0], galaxies[galaxy_from][1], galaxies[galaxy_to][1])
            galaxy_distances[key] = x_dist + y_dist

    print(sum(galaxy_distances.values()))


if __name__ == '__main__':
    main()
