import re

DIRECTIONS_LENGTH = 307
DIRECTION_MAPPING = {
    "L": 0,
    "R": 1
}


def setup() -> list[str]:
    file = open('map.txt', 'r')
    raw_map = file.read()
    file.close()
    return raw_map.split("\n\n")


def find_stop_point(node_name, directions_map, nodes: dict):
    step = 0
    while node_name[2] != "Z":
        c = directions_map[step % DIRECTIONS_LENGTH]
        step += 1
        node_name = nodes[node_name][DIRECTION_MAPPING[c]]
    return step


if __name__ == '__main__':
    directions, raw_nodes = setup()
    nodes = {}
    for line in raw_nodes.split("\n"):
        parts = re.match(r"(.+)\s=\s\((.+),\s(.+)\)", line)
        nodes[parts.group(1)] = (parts.group(2), parts.group(3))

    start_nodes = [k for k in nodes.keys() if k[2] == "A"]
    steps_to_end = [find_stop_point(node_name, directions, nodes) for node_name in start_nodes]
    cycles_to_end = [i / DIRECTIONS_LENGTH for i in steps_to_end]
    common_division_number = DIRECTIONS_LENGTH
    for i in cycles_to_end:
        common_division_number *= i

    print(int(common_division_number))
