from memory import Protocol
from memory import extract, Data, reduce
import logging

"""
Muster collects multiple requests for variables, dispatches the queries and
returns updated variables
"""
class Muster:
    def __init__(self, protocol: Protocol=None):
        self.__protocol = protocol or Protocol()

    """
    Query the wire protocol for a list of Variables and update the values in the
    variables
    """
    def update(self, variables: list):
        ranges = []
        datas = []
        for var in variables:
            ranges.append(var.range)
        for range in reduce(ranges):
            logging.debug("query: %s" % range)
            res = self.__protocol.query(range)
            datas.append(Data(range, res))
        for var in variables:
            var.bytes = extract(var.range, datas).bytes
