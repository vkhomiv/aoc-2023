def setup() -> list[str]:
    file = open('history.txt', 'r')
    data = file.readlines()
    file.close()
    return data


def calculate_set(sen_set):
    new_set = []
    set_iter = iter(sen_set)
    prev_elem = next(set_iter, None)
    if prev_elem is None:
        return []

    while (elem := next(set_iter, None)) is not None:
        new_set.append(elem - prev_elem)
        prev_elem = elem
    return new_set


if __name__ == '__main__':
    lines = setup()
    sensor_histories = [line.split() for line in lines]

    acc_part1 = 0
    acc_part2 = 0
    for sensor_history in sensor_histories:
        curr_set = [int(sensor_value) for sensor_value in sensor_history]
        pull_of_sets = []
        while not all(v == 0 for v in curr_set):
            pull_of_sets.append(curr_set[:])
            next_set = calculate_set(curr_set)
            curr_set = next_set

        for s in pull_of_sets:
            print(s)

        part1_pull = pull_of_sets[:]
        # part1
        diff = 0
        while len(part1_pull):
            curr_set = part1_pull.pop()
            diff += curr_set[-1:][0]
            print(diff)

        acc_part1 += diff

        part2_pull = pull_of_sets[:]
        # part2
        diff = 0
        while len(part2_pull):
            curr_set = part2_pull.pop()
            diff = curr_set[:-1][0] - diff
            print(diff)

        acc_part2 += diff

    print("End", acc_part1, acc_part2)
