import re
import sys

MAP_NAMES = (
    "seed-to-soil",
    "soil-to-fertilizer",
    "fertilizer-to-water",
    "water-to-light",
    "light-to-temperature",
    "temperature-to-humidity",
    "humidity-to-location",
)


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
        # TODO: cleanup
        nums = [int(x) for x in re.findall(r"\d+", s)]
        dst_start = nums[0]
        src_start = nums[1]
        self._src_ranges.append((src_start, src_start + nums[2] + 1))
        self._dst_ranges.append((dst_start, dst_start + nums[2] + 1))


maps = {name: Map() for name in MAP_NAMES}


with open(sys.argv[1]) as f:
    for line in f:
        if line == "\n":
            continue
        if line.startswith("seeds:"):
            seeds = frozenset(int(x) for x in re.findall(r"\d+", line))
        elif line.endswith("map:\n"):
            current_map = maps[re.match(r"([a-z-]+)", line).group(1)]
        else:
            current_map.add_range(line)

nums = set()

for s in seeds:
    current = s
    for name in (
        "seed-to-soil",
        "soil-to-fertilizer",
        "fertilizer-to-water",
        "water-to-light",
        "light-to-temperature",
        "temperature-to-humidity",
        "humidity-to-location",
    ):
        current = maps[name][current]
    nums.add(current)

print(min(nums))
