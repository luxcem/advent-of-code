import logging
import re
from pprint import pprint

test_input = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

cards_1 = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
cards_2 = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]

logger = logging.getLogger(__name__)

LINE_REGEX = re.compile(r"")


def get_hands_power(cards):
    cards_set = list(set(cards))
    if len(cards_set) == 1:
        return 10
    elif len(cards_set) == 2:
        # 4 of a kind
        if cards.count(cards_set[0]) == 4 or cards.count(cards_set[1]) == 4:
            return 9
        else:
            # Full house
            return 8
    elif len(cards_set) == 3:
        # 3 of a kind
        if (
            cards.count(cards_set[0]) == 3
            or cards.count(cards_set[1]) == 3
            or cards.count(cards_set[2]) == 3
        ):
            return 7
        # 2 pairs
        else:
            return 6
    elif len(cards_set) == 4:
        # 1 pair
        return 5
    else:
        # High card
        return 4


def fill_hands_power(hands):
    """Fill hands with combination power."""
    for hand in hands:
        cards, bid = hand
        hand.append(get_hands_power(cards))


def fill_hands_power_joker(hands):
    for hand in hands:
        cards, bid = hand
        if "J" in cards:
            # Replace joker by all possible cards and get best power
            max_power = 0
            for card in cards_2:
                power = get_hands_power(cards.replace("J", card))
                max_power = max(max_power, power)
            hand.append(max_power)
        else:
            hand.append(get_hands_power(cards))


def order_hands(hands, order):
    # Order hands by power then by best high card (left to right)
    hands.sort(
        key=lambda x: (
            x[2],
            order.index(x[0][0]),
            order.index(x[0][1]),
            order.index(x[0][2]),
            order.index(x[0][3]),
            order.index(x[0][4]),
        ),
        reverse=False,
    )
    return hands


def part1(text_input: str) -> str:
    result = 0
    hands = []
    for line in text_input.strip().split("\n"):
        hand, bid = line.split()
        hands.append([hand, bid])

    fill_hands_power(hands)
    order_hands(hands, cards_1)
    # Multiply hands rank by its bid
    pprint(hands)
    for i, hand in enumerate(hands):
        result += (i + 1) * int(hand[1])
    return str(result)


def part2(text_input: str) -> str:
    result = 0
    hands = []
    for line in text_input.strip().split("\n"):
        hand, bid = line.split()
        hands.append([hand, bid])

    fill_hands_power_joker(hands)
    order_hands(hands, cards_2)
    # Multiply hands rank by its bid
    pprint(hands)
    for i, hand in enumerate(hands):
        result += (i + 1) * int(hand[1])
    return str(result)
