from exception import *
from memory import Data, Range

def extract(range: Range, datas: list) -> Data:
    for data in datas:
        d = _extract(range, data)
        if d:
            return Data(range, d)
    raise NotFoundException("%s was not found" % (range))


def _extract(range: Range, data: list) -> bytes:
    start = (range.address - data.range.address) * 2
    end = start + range.words * 2
    if end > len(data.bytes) or start < 0:
        return None
    return data.bytes[start:end]
