import dataclasses
import re
import sys
from collections.abc import Iterable
from typing import Pattern
from typing import Self


@dataclasses.dataclass(frozen=True, slots=True)
class Card:
    winning_numbers: frozenset[str]

    @classmethod
    def from_string(cls, s: str, pat: Pattern[str] = re.compile(r"(\d+)\s+")) -> Self:
        return cls(winning_numbers=frozenset(pat.findall(s)))

    def count_winning_numbers(self, nums: Iterable[str]) -> int:
        return len(self.winning_numbers.intersection(nums))


def get_points(num: int) -> int:
    return num if num < 2 else 2 ** (num - 1)


def get_my_numbers(s: str, pat: Pattern[str] = re.compile(r"(\d+)")) -> list[str]:
    return pat.findall(s)


def get_points_from_line(s: str) -> int:
    a, _, b = s.partition("|")
    card = Card.from_string(a)
    num_winning_numbers = card.count_winning_numbers(get_my_numbers(b))
    return get_points(num_winning_numbers)


with open(sys.argv[1]) as f:
    print(sum(get_points_from_line(line) for line in f))
