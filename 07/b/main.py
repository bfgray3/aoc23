import collections
import enum
import functools
import sys


class HandType(enum.Enum):
    FIVE_OF_A_KIND = enum.auto()
    FOUR_OF_A_KIND = enum.auto()
    FULL_HOUSE = enum.auto()
    THREE_OF_A_KIND = enum.auto()
    TWO_PAIR = enum.auto()
    ONE_PAIR = enum.auto()
    HIGH_CARD = enum.auto()


class Hand:
    CARD_DICT = dict(zip("AKQT98765432J", range(13)))

    def __init__(self, s: str, bid: str) -> None:
        self._cards = s
        self._bid = int(bid)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        if self.hand_type != other.hand_type:
            return self.hand_type.value > other.hand_type.value
        for this, opponent in zip(self._cards, other._cards):
            if this != opponent:
                return self.CARD_DICT[this] > self.CARD_DICT[opponent]
        raise ValueError

    def get_winnings(self, rank: int) -> int:
        return rank * self._bid

    @classmethod
    def _process_jokers(cls, s: str) -> str:
        if "J" not in s:
            return s
        elif s == "J" * 5:
            return "A" * 5

        counter = collections.Counter(s.replace("J", ""))
        counts = sorted(counter.values())

        if len(counts) == 1:
            (card,) = counter
            return card * 5

        num_unique_non_jokers = len(set(counts))

        if num_unique_non_jokers == 1:
            card = max(counter, key=cls.CARD_DICT.get)
            return s.replace("J", card)
        elif num_unique_non_jokers > 1:
            (card_and_count,) = counter.most_common(1)
            return s.replace("J", card_and_count[0])
        raise ValueError

    @functools.cached_property
    def hand_type(self) -> HandType:
        cards = self._process_jokers(self._cards)
        counts = sorted(collections.Counter(cards).values())
        if counts == [5]:
            return HandType.FIVE_OF_A_KIND
        elif counts == [1, 4]:
            return HandType.FOUR_OF_A_KIND
        elif counts == [2, 3]:
            return HandType.FULL_HOUSE
        elif counts == [1, 1, 3]:
            return HandType.THREE_OF_A_KIND
        elif counts == [1, 2, 2]:
            return HandType.TWO_PAIR
        elif counts == [1, 1, 1, 2]:
            return HandType.ONE_PAIR
        elif counts == [1, 1, 1, 1, 1]:
            return HandType.HIGH_CARD
        else:
            raise ValueError


with open(sys.argv[1]) as f:
    hands = [Hand(*line.split()) for line in f]

hands.sort()

print(sum(h.get_winnings(rank=i) for i, h in enumerate(hands, start=1)))
