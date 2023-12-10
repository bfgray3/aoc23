import dataclasses
import enum
import re
import sys
from typing import Pattern
from typing import Self


class Color(enum.StrEnum):
    BLUE = enum.auto()
    GREEN = enum.auto()
    RED = enum.auto()


TOTAL_COUNTS = {
    Color.BLUE: 14,
    Color.GREEN: 13,
    Color.RED: 12,
}

COUNT_REGEXPS = {c: re.compile(rf"(\d+)\s+{c}") for c in Color}


@dataclasses.dataclass(frozen=True, slots=True)
class Draw:
    draws: dict[Color, int]

    @classmethod
    def from_str(cls, s: str) -> Self:
        return cls(draws={c: cls._count_color(s, c) for c in Color})

    @property
    def is_valid(self) -> bool:
        return all(v <= TOTAL_COUNTS[k] for k, v in self.draws.items())

    @staticmethod
    def _count_color(s: str, c: Color) -> int:
        try:
            return int(COUNT_REGEXPS[c].search(s).group(1))
        except AttributeError:
            return 0


def get_game_id(s: str, pat: Pattern[str] = re.compile(r"^Game\s+(\d+)")) -> int:
    return int(pat.match(line).group(1))


id_sum = 0

with open(sys.argv[1]) as f:
    for line in f:
        draws = (Draw.from_str(s) for s in line.split(";"))
        if all(d.is_valid for d in draws):
            id_sum += get_game_id(line)

print(id_sum)
