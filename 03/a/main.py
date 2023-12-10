import dataclasses
import re
import sys
from collections.abc import Iterable
from typing import Pattern


@dataclasses.dataclass(frozen=True, slots=True)
class Number:
    row: int
    num: int
    start: int
    end: int

    def is_adjacent_to_symbol(self, symbol_dict: dict[int, Iterable[int]]) -> bool:
        for x in (self.start - 1, self.end):
            if self.row in symbol_dict and x in symbol_dict[self.row]:
                return True
        for r in (self.row - 1, self.row + 1):
            for i in range(self.start - 1, self.end + 1):
                if r in symbol_dict and i in symbol_dict[r]:
                    return True
        return False


def find_numbers(
    x: Iterable[str], pat: Pattern[str] = re.compile(r"(\d+)")
) -> list[Number]:
    return [
        Number(i, int(m.group(1)), *m.span())
        for i, r in enumerate(x)
        for m in pat.finditer(r)
    ]


def is_symbol(s: str) -> bool:
    return not s.isdigit() and s != "."


with open(sys.argv[1]) as f:
    schematic = [line.strip() for line in f]


symbols = {
    i: [j for j, x in enumerate(row) if is_symbol(x)] for i, row in enumerate(schematic)
}

print(sum(n.num for n in find_numbers(schematic) if n.is_adjacent_to_symbol(symbols)))
