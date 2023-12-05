import dataclasses
import re
import sys
from collections import defaultdict
from typing import Iterable
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


def get_my_numbers(s: str, pat: Pattern[str] = re.compile(r"(\d+)")) -> list[str]:
    return pat.findall(s)


def get_num_matching_numbers_from_line(s: str) -> int:
    a, _, b = s.partition("|")
    card = Card.from_string(a)
    return card.count_winning_numbers(get_my_numbers(b))


counts = defaultdict(lambda: 1)

with open(sys.argv[1]) as f:
    for i, line in enumerate(f, start=1):
        matching_numbers = get_num_matching_numbers_from_line(line)
        for card in range(i + 1, i + matching_numbers + 1):
            counts[card] += counts[i]

print(sum(counts[j] for j in range(1, i + 1)))
