import re
import sys
from typing import Pattern

DIGIT_MAP = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def string_to_num(s: str) -> int:
    return DIGIT_MAP[s] if s in DIGIT_MAP else int(s)


def get_number(
    s: str, pat: Pattern[str] = re.compile(rf"(?=({'|'.join(DIGIT_MAP)}|\d))")
) -> int:
    matches = pat.findall(s)
    return 10 * string_to_num(matches[0]) + string_to_num(matches[-1])


with open(sys.argv[1]) as f:
    print(sum(get_number(line) for line in f))
