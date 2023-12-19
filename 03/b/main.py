import dataclasses
import functools
import operator
import re
import sys
from collections.abc import Iterable
from typing import Mapping
from typing import Pattern


GEAR_SYMBOL = "*"
GEAR_ADJACENCY_COUNT = 2


@dataclasses.dataclass(frozen=True, slots=True)
class Number:
    row: int
    num: int
    start: int
    end: int


def find_numbers(
    x: Iterable[str], pat: Pattern[str] = re.compile(r"(\d+)")
) -> dict[int, list[Number]]:
    return {
        i: [Number(i, int(m.group(1)), *m.span()) for m in pat.finditer(r)]
        for i, r in enumerate(x)
    }


@dataclasses.dataclass(frozen=True, slots=True)
class Star:
    row: int
    column: int

    def is_gear(self, numbers: Mapping[int, list[Number]]) -> bool:
        return len(self._adjacent_numbers(numbers)) == GEAR_ADJACENCY_COUNT

    def _adjacent_numbers(self, numbers: Mapping[int, list[Number]]) -> list[int]:
        adjacent_numbers = []
        for num in numbers[self.row]:
            if num.start == self.column + 1 or num.end == self.column:
                adjacent_numbers.append(num)
        for r in (self.row - 1, self.row + 1):
            try:
                for num in numbers[r]:
                    if num.start - 1 <= self.column <= num.end:
                        adjacent_numbers.append(num)
            except KeyError:
                pass
        return [n.num for n in adjacent_numbers]

    def gear_ratio(self, numbers: Mapping[int, list[Number]]) -> int:
        return functools.reduce(operator.mul, self._adjacent_numbers(numbers))


with open(sys.argv[1]) as f:
    schematic = [line.strip() for line in f]

numbers = find_numbers(schematic)

stars = [  # i is row, j is column
    Star(row=i, column=j)
    for i, row in enumerate(schematic)
    for j, x in enumerate(row)
    if x == "*"
]

print(sum(s.gear_ratio(numbers) for s in stars if s.is_gear(numbers)))
