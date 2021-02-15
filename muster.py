from protocol import Protocol
from memory import extract
from memory import reduce

"""
Muster collects multiple requests for variables, dispatches the queries and
returns updated variables
"""
class Muster:
    def __init__(self, protocol: Protocol):
        self.__protocol = protocol

    """
    Query the wire protocol for a list of Variables and update the values in the
    variables
    """
    def update(self, variables: list):
        #for var in variables:
        #    var.bytes = self.__protocol.query(var.range.address, var.range.words - 1)
        #return
        ranges = []
        for var in variables:
            ranges.append(var.range)
        for range in reduce(ranges):
            response = self.__protocol.query(range.address, range.words - 1)
            for var in variables:
                var.bytes = extract(range, var.range, response)
