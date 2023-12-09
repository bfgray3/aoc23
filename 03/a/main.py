import dataclasses
import re
import sys
from collections.abc import Iterable


@dataclasses.dataclass
class Number:
    row: int
    num: str
    start: int
    end: int

    def is_adjacent_to_symbol(self, symbol_dict: dict[int, list[int]]) -> bool:
        for r in (self.row - 1, self.row + 1):
            for i in range(self.start - 1, self.end + 1):
                try:
                    if i in symbol_dict[r]:
                        return True
                except KeyError:
                    pass
        for x in (self.start - 1, self.end):
            try:
                if x in symbol_dict[self.row]:
                    return True
            except KeyError:
                pass
        return False


def find_numbers(x: Iterable[str]) -> list[Number]:
    return [
        Number(i, m.group(1), *m.span())
        for i, r in enumerate(x)
        for m in re.finditer(r"(\d+)", r)
    ]


def is_symbol(s: str) -> bool:
    return not s.isdigit() and s != "."


with open(sys.argv[1]) as f:
    schematic = [line.strip() for line in f]


symbols = {
    i: [j for j, x in enumerate(row) if is_symbol(x)] for i, row in enumerate(schematic)
}

print(
    sum(int(n.num) for n in find_numbers(schematic) if n.is_adjacent_to_symbol(symbols))
)
