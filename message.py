from dataclasses import dataclass
from typing import Any


@dataclass
class Message:
    """
    A message from client

    Representation invariables:
        type: the type of message
        command: the specific command player sends
        data: any data in the message (if required)
        priority: the order of message in message queue,
                  lower value for higher priority
    """
    type: int
    command: int
    data: Any
    priority: int


"""
Message Types
"""
TYPE_CONNECT = 1
TYPE_MOVE = 10
TYPE_FIRE = 11
TYPE_SENSE = 12
TYPE_GADGET = 13

"""
Message Commands
"""
CONNECT = 1
