import dataclasses
import re
import sys
from typing import Iterable
from typing import Self


@dataclasses.dataclass(frozen=True, slots=True)
class Card:
    winning_numbers: frozenset[str]

    @classmethod
    def from_string(cls, s: str) -> Self:
        # TODO: clean up so don't need .strip()
        return cls(
            winning_numbers=frozenset(x.strip() for x in re.findall(r"(\d+\s+)", s))
        )

    def count_winning_numbers(self, nums: Iterable[str]) -> int:
        return len(self.winning_numbers.intersection(nums))


def get_points(num: int) -> int:
    if num < 2:
        return num
    return 2 ** (num - 1)


def get_my_numbers(s: str) -> list[str]:
    return re.findall(r"(\d+)", s)


points = 0

with open(sys.argv[1]) as f:
    for line in f:
        a, _, b = line.partition("|")
        card = Card.from_string(a)
        num_winning_numbers = card.count_winning_numbers(get_my_numbers(b))
        points += get_points(num_winning_numbers)

print(points)
