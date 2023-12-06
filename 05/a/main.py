import re
import sys
from typing import Pattern

MAP_NAMES = (
    "seed-to-soil",
    "soil-to-fertilizer",
    "fertilizer-to-water",
    "water-to-light",
    "light-to-temperature",
    "temperature-to-humidity",
    "humidity-to-location",
)

NAME_PATTERN = re.compile(r"([a-z-]+)")


class Map:
    def __init__(self) -> None:
        self._src_ranges = []
        self._dst_ranges = []

    def __getitem__(self, idx: int) -> int:
        for i, rng in enumerate(self._src_ranges):
            if rng[0] <= idx <= rng[1]:
                return self._dst_ranges[i][0] + idx - rng[0]
        return idx

    def add_range(self, s: str) -> None:
        dst_start, src_start, length = get_numbers(s)
        self._src_ranges.append((src_start, src_start + length + 1))
        self._dst_ranges.append((dst_start, dst_start + length + 1))


def get_numbers(s: str, pat: Pattern[str] = re.compile(r"\d+")) -> list[int]:
    return [int(x) for x in pat.findall(s)]


maps = {name: Map() for name in MAP_NAMES}


with open(sys.argv[1]) as f:
    for line in f:
        if line == "\n":
            continue
        elif line.startswith("seeds:"):
            seeds = get_numbers(line)
        elif line.endswith("map:\n"):
            current_map = maps[NAME_PATTERN.match(line).group(1)]
        else:
            current_map.add_range(line)

nums = set()

for s in seeds:
    current = s
    for name in MAP_NAMES:
        current = maps[name][current]
    nums.add(current)

print(min(nums))
