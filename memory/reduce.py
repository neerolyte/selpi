from memory import Range

# Maximum number of words that can retrieved at one time
MAX_WORDS=256

"""
Combine a set of memory ranges in to a list of ranges that can sent
"""
def reduce(ranges: list) -> list:
    return _reduce(sorted(ranges))

def _reduce(ranges: list) -> list:
    if len(ranges) <= 1:
        return ranges
    r1 = ranges[0]
    r2 = ranges[1]
    words = r2.address - r1.address + r2.words
    if words > MAX_WORDS:
        return [r1] + _reduce(ranges[1:])
    return _reduce([Range(r1.address, words)] + ranges[2:])
