import re


class GameSet:
    red_cubes: int
    green_cubes: int
    blue_cubes: int

    def __init__(self, red_cubes, green_cubes, blue_cubes):
        self.red_cubes = red_cubes
        self.green_cubes = green_cubes
        self.blue_cubes = blue_cubes

    def __repr__(self):
        return f"r={self.red_cubes}, g={self.green_cubes}, b={self.blue_cubes}"

    def power(self):
        return self.red_cubes * self.green_cubes * self.blue_cubes


class Game:
    game_id: int
    is_possible: bool
    sets: [GameSet]
    min_set: GameSet

    def __init__(self, game_id, sets):
        self.game_id = game_id
        self.sets = sets
        self.is_possible = False

    def __repr__(self):
        return f"id={self.game_id}, is_possible={self.is_possible}"


RED_CUBES_MAX = 12
GREEN_CUBES_MAX = 13
BLUE_CUBES_MAX = 14

games: [Game] = []


def setup():
    file = open('games_log.txt', 'r')
    games_input = file.readlines()
    for game_line in games_input:
        game_id = int((re.search(r'Game (\d+):', game_line)).group(1))
        game_sets = []
        for game_set in game_line.split(';'):
            red_cubes_match = re.search(r'(\d+) red', game_set)
            red_cubes = 0 if not red_cubes_match else int(red_cubes_match.group(1))
            green_cubes_match = re.search(r'(\d+) green', game_set)
            green_cubes = 0 if not green_cubes_match else int(green_cubes_match.group(1))
            blue_cubes_match = re.search(r'(\d+) blue', game_set)
            blue_cubes = 0 if not blue_cubes_match else int(blue_cubes_match.group(1))
            game_sets.append(GameSet(red_cubes, green_cubes, blue_cubes))
        games.append(Game(game_id, game_sets))


def find_possible_games():
    for game in games:
        this_game_is_possible = True
        max_red = 0
        max_green = 0
        max_blue = 0
        for game_set in game.sets:

            # part2
            if game_set.red_cubes > max_red:
                max_red = game_set.red_cubes
            if game_set.green_cubes > max_green:
                max_green = game_set.green_cubes
            if game_set.blue_cubes > max_blue:
                max_blue = game_set.blue_cubes

            # part1
            if game_set.red_cubes > RED_CUBES_MAX:
                this_game_is_possible = False
            if game_set.green_cubes > GREEN_CUBES_MAX:
                this_game_is_possible = False
            if game_set.blue_cubes > BLUE_CUBES_MAX:
                this_game_is_possible = False
        game.is_possible = this_game_is_possible
        game.min_set = GameSet(max_red, max_green, max_blue)


def calculate_result():
    part1_acc = 0
    part2_acc = 0
    for game in games:
        part1_acc += game.game_id if game.is_possible else 0
    for game in games:
        part2_acc += game.min_set.power()
    return part1_acc, part2_acc


if __name__ == '__main__':
    setup()
    find_possible_games()
    print(calculate_result())
