import dataclasses
import enum
import functools
import operator
import re
import sys
from typing import Self


class Color(enum.StrEnum):
    BLUE = enum.auto()
    GREEN = enum.auto()
    RED = enum.auto()


COUNT_REGEXPS = {c: re.compile(rf"(\d+)\s+{c}") for c in Color}


@dataclasses.dataclass(frozen=True, slots=True)
class Draw:
    draws: dict[Color, int]

    @classmethod
    def from_str(cls, s: str) -> Self:
        return cls(draws={c: cls._count_color(s, c) for c in Color})

    @staticmethod
    def _count_color(s: str, c: Color) -> int:
        if m := COUNT_REGEXPS[c].search(s):
            return int(m.group(1))
        return 0


power_sum = 0

with open(sys.argv[1]) as f:
    for line in f:
        draws = [Draw.from_str(s) for s in line.split(";")]
        power_sum += functools.reduce(
            operator.mul,
            (max(d.draws[c] for d in draws) for c in Color),
        )

print(power_sum)
