import sys
import re


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

REGEX = re.compile(rf"(?=({'|'.join(DIGIT_MAP.keys())}|\d))")


def string_to_num(s: str) -> int:
    return DIGIT_MAP[s] if s in DIGIT_MAP else int(s)


def get_number(s: str) -> int:
    matches = REGEX.findall(s)
    first = string_to_num(matches[0])
    second = string_to_num(matches[-1])
    print(f"{s=}, {first=}, {second=}")
    return 10 * first + second


with open(sys.argv[1]) as f:
    document = [line.strip() for line in f]


print(sum(get_number(line) for line in document))
