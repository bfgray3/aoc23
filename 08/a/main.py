import itertools
import re
import sys

nodes = {}

with open(sys.argv[1]) as f:
    for line in f:
        if line == "\n":
            continue
        if "=" not in line:
            instructions = line.strip()
        else:
            (info,) = re.findall(r"([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)", line)
            nodes[info[0]] = (info[1], info[2])

current = "AAA"

for i, direction in enumerate(itertools.cycle(instructions)):
    if current == "ZZZ":
        break
    else:
        current = nodes[current][0 if direction == "L" else 1]

print(i)
