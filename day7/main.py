from collections import defaultdict

CARD_RANKS = {"A": 13,
              "K": 12,
              "Q": 11,
              "J": 0,
              "T": 9,
              "9": 8,
              "8": 7,
              "7": 6,
              "6": 5,
              "5": 4,
              "4": 3,
              "3": 2,
              "2": 1,
              }

FIVE_IN_HAND_POWER = 7

power_config = {
    (5,): FIVE_IN_HAND_POWER,
    (4, 1): 6,
    (3, 2): 5,
    (3, 1, 1): 4,
    (2, 2, 1): 3,
    (2, 1, 1, 1): 2,
    (1, 1, 1, 1, 1): 1
}


class Hand:
    hand: str
    bid: int
    power: int

    def __init__(self, raw_hand: str):
        hand, bid = raw_hand.split()
        self.hand = hand
        self.bid = int(bid)

        curr_power = defaultdict(int)
        for c in self.hand:
            curr_power[c] += 1

        if "J" not in curr_power:
            self.power = power_config[tuple(sorted(curr_power.values(), reverse=True))]
        elif curr_power["J"] == 5:
            self.power = FIVE_IN_HAND_POWER
        else:
            jokers_count = curr_power["J"]
            del curr_power["J"]
            hand_results = sorted(curr_power.values(), reverse=True)
            result = [hand_results[0] + jokers_count] + hand_results[1:]
            self.power = power_config[tuple(result)]

    def __lt__(self, other):
        if self.power != other.power:
            return self.power < other.power

        for i in range(5):
            if CARD_RANKS[self.hand[i]] == CARD_RANKS[other.hand[i]]:
                continue
            else:
                return CARD_RANKS[self.hand[i]] < CARD_RANKS[other.hand[i]]

    def __repr__(self):
        return "%s %s %s" % (self.power, self.hand, self.bid)


def setup() -> list[str]:
    file = open('cards.txt', 'r')
    lines = file.readlines()
    file.close()
    return lines


if __name__ == '__main__':
    raw_hands = setup()
    hands = sorted([Hand(hand) for hand in raw_hands])

    winnings = [hand.bid * (idx + 1) for idx, hand in enumerate(hands)]
    print(sum(winnings))
