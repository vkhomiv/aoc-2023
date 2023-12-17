import enum
from typing import Optional

VISUAL_MAPPER = {
    'F': '┌',
    "L": '└',
    "7": '┐',
    "J": '┘',
    "|": "│",
    "-": "─"
}


class DIRECTION(enum.Enum):
    TOP = "top"
    RIGHT = "right"
    BOTTOM = "bottom"
    LEFT = "left"


OPPOSITE_MAPPING = {
    DIRECTION.TOP: DIRECTION.BOTTOM,
    DIRECTION.BOTTOM: DIRECTION.TOP,
    DIRECTION.LEFT: DIRECTION.RIGHT,
    DIRECTION.RIGHT: DIRECTION.LEFT
}


class Tile:
    x: int
    y: int
    value: str
    path_length: Optional[int]
    direction: Optional[dict]

    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.path_length = None
        self.direction = None

    def __repr__(self):
        # return f"{self.value}{self.direction or ' '}"
        d = self.direction
        r = f"{VISUAL_MAPPER[self.value] if self.value in VISUAL_MAPPER else self.value}"
        # if self.direction:
        #     if d["from"] == DIRECTION.RIGHT and d["to"] == DIRECTION.LEFT:
        #         r = "<"
        #     elif d["to"] == DIRECTION.RIGHT and d["from"] == DIRECTION.LEFT:
        #         r = ">"
        #     elif d["from"] == DIRECTION.TOP and d["to"] == DIRECTION.BOTTOM:
        #         r = "v"
        #     elif d["to"] == DIRECTION.TOP and d["from"] == DIRECTION.BOTTOM:
        #         r = "^"
        return r


class MazeContext:
    start_tile: Tile
    x_max: int
    y_max: int
    maze: [str]
    maze_map: [[Tile]]

    def __init__(self, x_max, y_max, start_tile, maze_map):
        self.start_tile = start_tile
        self.x_max = x_max
        self.y_max = y_max
        self.maze_map = maze_map

    def get_farthest_tile(self):
        farthest_path = None
        for y in range(self.y_max):
            for x in range(self.x_max):
                min_path = self.maze_map[y][x].path_length or 0
                if not farthest_path or min_path > farthest_path:
                    farthest_path = min_path
        return farthest_path

    def _get_left(self, tile: Tile) -> Optional[Tile]:
        x_left = tile.x - 1
        if x_left < 0:
            return None
        left_tile = self.maze_map[tile.y][x_left]

        if left_tile.value in ['.', '|', '7', 'J']:
            return None

        from_left_to_mapping = {
            "-": DIRECTION.LEFT,
            "F": DIRECTION.BOTTOM,
            "L": DIRECTION.TOP
        }
        left_tile.direction = {"from": DIRECTION.RIGHT, "to": from_left_to_mapping[left_tile.value]}
        return left_tile

    def _get_top(self, tile: Tile) -> Optional[Tile]:
        y_top = tile.y - 1
        if y_top < 0:
            return None

        top_tile = self.maze_map[y_top][tile.x]
        if top_tile.value in ['.', '-', 'J', 'L']:
            return None

        from_top_to_mapping = {
            "|": DIRECTION.TOP,
            "F": DIRECTION.RIGHT,
            "7": DIRECTION.LEFT
        }
        top_tile.direction = {"from": DIRECTION.BOTTOM, "to": from_top_to_mapping[top_tile.value]}

        return top_tile

    def _get_right(self, tile: Tile) -> Optional[Tile]:
        x_right = tile.x + 1
        if x_right == self.x_max:
            return None

        right_tile = self.maze_map[tile.y][x_right]
        if right_tile.value in ['.', '|', 'L', 'F']:
            return None

        from_right_to_mapping = {
            "-": DIRECTION.RIGHT,
            "J": DIRECTION.TOP,
            "7": DIRECTION.BOTTOM
        }
        right_tile.direction = {"from": DIRECTION.LEFT, "to": from_right_to_mapping[right_tile.value]}

        return right_tile

    def _get_bottom(self, tile: Tile) -> Optional[Tile]:
        y_bottom = tile.y + 1
        if y_bottom == self.y_max:
            return None

        bottom_tile = self.maze_map[y_bottom][tile.x]
        if bottom_tile.value in ['.', '-', '7', 'F']:
            return None

        from_bottom_to_mapping = {
            "|": DIRECTION.BOTTOM,
            "J": DIRECTION.LEFT,
            "L": DIRECTION.RIGHT
        }
        bottom_tile.direction = {"from": DIRECTION.TOP, "to": from_bottom_to_mapping[bottom_tile.value]}

        return bottom_tile

    def get_next_by_direction(self, tile: Tile) -> Tile:
        direction = tile.direction["to"]
        if direction == DIRECTION.LEFT:
            return self.maze_map[tile.y][tile.x - 1]
        elif direction == DIRECTION.RIGHT:
            return self.maze_map[tile.y][tile.x + 1]
        elif direction == DIRECTION.TOP:
            return self.maze_map[tile.y - 1][tile.x]
        else:
            return self.maze_map[tile.y + 1][tile.x]

    def find_path_tile_at_right(self, tile: Tile) -> Optional[Tile]:
        right_border_x = self.x_max - 1
        if tile.x == right_border_x:
            return None
        curr_tile = tile
        while curr_tile.x < right_border_x:
            next_tile = self.maze_map[curr_tile.y][curr_tile.x + 1]
            if next_tile.direction:
                return next_tile
            curr_tile = next_tile
        return None

    def get_path_direction(self) -> DIRECTION:
        left_turns = 0
        right_turns = 0

        curr_tile = self.start_tile

        while next_tile := self.get_next_by_direction(curr_tile):
            t_from = next_tile.direction["from"]
            t_to = next_tile.direction["to"]
            if t_from == DIRECTION.LEFT and t_to == DIRECTION.BOTTOM \
                    or t_from == DIRECTION.TOP and t_to == DIRECTION.LEFT \
                    or t_from == DIRECTION.RIGHT and t_to == DIRECTION.TOP \
                    or t_from == DIRECTION.BOTTOM and t_to == DIRECTION.RIGHT:
                right_turns += 1
            elif t_from == DIRECTION.LEFT and t_to == DIRECTION.TOP \
                    or t_from == DIRECTION.TOP and t_to == DIRECTION.RIGHT \
                    or t_from == DIRECTION.RIGHT and t_to == DIRECTION.BOTTOM \
                    or t_from == DIRECTION.BOTTOM and t_to == DIRECTION.LEFT:
                left_turns += 1
            curr_tile = next_tile
            if curr_tile == self.start_tile:
                break

        print(left_turns, right_turns)
        return DIRECTION.LEFT if left_turns > right_turns else DIRECTION.RIGHT

    def get_first_and_last_tiles(self) -> [Tile]:
        tiles = [
            self._get_top(self.start_tile),
            self._get_right(self.start_tile),
            self._get_bottom(self.start_tile),
            self._get_left(self.start_tile)
        ]
        first_and_last: [Tile] = [tile for tile in tiles if tile]
        last = first_and_last[1]
        last.direction = {"from": last.direction["to"], "to": last.direction["from"]}
        return first_and_last[0], last

    def init_next(self, tile: Tile) -> Tile:
        init_mapping = {
            DIRECTION.LEFT: self._get_left,
            DIRECTION.TOP: self._get_top,
            DIRECTION.RIGHT: self._get_right,
            DIRECTION.BOTTOM: self._get_bottom,
        }

        return init_mapping[tile.direction["to"]](tile)

    def __repr__(self):
        # out = [f"size:{x_max}x{y_max} start:({x_start},{y_start})"]
        out = []
        for line in self.maze_map:
            out.append("".join([str(s) for s in line]))

        return "\n".join(out)


def setup() -> list[str]:
    file = open('maze.txt', 'r')
    data = file.readlines()
    file.close()
    return [s.strip() for s in data]


def find_start(maze_map):
    for y in range(len(maze_map)):
        for x in range(len(maze_map[y])):
            tile = maze_map[y][x]
            if tile.value == "S":
                return tile
    return None


def is_nest(path_direction: DIRECTION, tile: Tile):
    t_from = tile.direction["from"]
    t_to = tile.direction["to"]

    if path_direction == DIRECTION.RIGHT:
        return t_from == DIRECTION.TOP and t_to in [DIRECTION.BOTTOM, DIRECTION.RIGHT, DIRECTION.LEFT] \
            or t_to == DIRECTION.BOTTOM and t_from in [DIRECTION.RIGHT, DIRECTION.LEFT, DIRECTION.TOP]
    else:
        return t_from == DIRECTION.BOTTOM and t_to in [DIRECTION.LEFT, DIRECTION.TOP, DIRECTION.RIGHT] \
            or t_to == DIRECTION.TOP and t_from in [DIRECTION.LEFT, DIRECTION.RIGHT, DIRECTION.BOTTOM]


def main():
    maze = setup()
    y_max = len(maze)
    x_max = len(maze[0])
    maze_map = [[Tile(x, y, maze[y][x]) for x in range(x_max)] for y in range(y_max)]
    start_tile = find_start(maze_map)
    context = MazeContext(x_max, y_max, start_tile, maze_map)

    [first_tile, last_tile] = context.get_first_and_last_tiles()
    start_tile.direction = {"from": OPPOSITE_MAPPING[last_tile.direction["to"]],
                            "to": OPPOSITE_MAPPING[first_tile.direction["from"]]}
    tile = first_tile

    while tile != last_tile:
        tile = context.init_next(tile)

    path_direction = context.get_path_direction()

    items_in_nest = 0
    for y in range(y_max):
        for x in range(x_max):
            tile: Tile = maze_map[y][x]
            if tile.direction:
                continue
            # print(tile.x, tile.y)

            path_tile = context.find_path_tile_at_right(tile)
            tile.value = "O"
            if path_tile and is_nest(path_direction, path_tile):
                tile.value = "I"
                items_in_nest += 1

    print(path_direction)
    print(context)
    print(items_in_nest)


if __name__ == '__main__':
    main()
