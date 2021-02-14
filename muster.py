from protocol import Protocol
from variable import Variable

"""
Muster collects multiple requests for variables, dispatches the queries and
returns updated variables
"""
class Muster:
    def __init__(self, protocol: Protocol):
        self.__protocol = protocol

    """
    Query the wire protocol for a list of Variables
    return the same variables with updated values
    """
    def query(self, variables: list):
        rvariables = []
        for var in variables:
            response = self.__protocol.query(var.get_address(), var.get_words() - 1)
            rvariables.append(var.set_bytes(response))
        return rvariables
