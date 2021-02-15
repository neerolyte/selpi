from exception import *

def extract(haystack, needle, bytes: bytes) -> bytes:
    start = (needle.address - haystack.address) * 2
    end = start + needle.words * 2
    if end > len(bytes):
        raise OutOfBoundsException("%s is outside of %s" % (needle, haystack))
    return bytes[start:end]
