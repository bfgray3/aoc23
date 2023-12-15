import itertools
import re
import sys

nodes = {}
current = "AAA"

LINE_REGEX = re.compile(r"([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)")

with open(sys.argv[1]) as f:
    for line in f:
        if line == "\n":
            continue
        elif "=" in line:
            (info,) = LINE_REGEX.findall(line)
            nodes[info[0]] = (info[1], info[2])
        else:
            instructions = line.strip()

for i, direction in enumerate(itertools.cycle(instructions)):
    if current == "ZZZ":
        break
    current = nodes[current][int(direction == "R")]

print(i)
