import re


def isCorrectGroup(group: str) -> bool:
    pattern = r'^\d{3}-\d{3}$'
    return bool(re.match(pattern, group))

