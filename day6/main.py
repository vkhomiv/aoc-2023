def setup() -> list[str]:
    file = open('sheet_of_paper.txt', 'r')
    lines = file.readlines()
    file.close()
    return lines


def setup_for_silver_star() -> list[tuple]:
    lines = setup()
    times = lines[0].split()[1:]
    distances = lines[1].split()[1:]
    return [(int(times[idx]), int(distances[idx])) for idx in range(len(times))]


def setup_for_gold_star() -> tuple:
    lines = setup()
    time = lines[0].split(":")[1].replace(" ", "")
    distances = lines[1].split(":")[1].replace(" ", "")
    return int(time), int(distances)


def find_win_count(time, distance):
    win_count = 0
    for speed in range(time):
        cur_distance = speed * (time - speed)
        if cur_distance > distance:
            win_count += 1
    return win_count


def get_the_silver_star():
    races = setup_for_silver_star()
    multiplied_wins = 1
    for time, distance in races:
        multiplied_wins *= find_win_count(time, distance)
    print(multiplied_wins)


def get_the_gold_star():
    time, distance = setup_for_gold_star()
    print(find_win_count(time, distance))


if __name__ == '__main__':
    get_the_silver_star()
    get_the_gold_star()
