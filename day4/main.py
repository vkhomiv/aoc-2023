import re
from collections import defaultdict


def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))


def setup():
    file = open("cards.txt", "r")
    data = file.readlines()
    file.close()
    return data


def count_cards(lines):
    score = 0
    cards_copies = defaultdict(lambda: 1)
    for idx, line in enumerate(lines):
        winning_numbers = re.search(r":(.*)\|", line).group(1).split()
        numbers = re.search(r"\|(.*)$", line).group(1).split()
        own_winning_numbers = intersection(winning_numbers, numbers)
        own_winning_numbers_count = len(own_winning_numbers)
        current_card_number = idx + 1
        card_multiplier = cards_copies[current_card_number]

        # part1
        if own_winning_numbers_count > 0:
            score += pow(2, own_winning_numbers_count - 1)

        # part2
        for card_number in range(current_card_number + 1, own_winning_numbers_count + current_card_number + 1):
            cards_copies[card_number] += card_multiplier

    return score, sum(cards_copies.values())


if __name__ == '__main__':
    input_lines = setup()
    score, cards_count = count_cards(input_lines)
    print(score, cards_count)
