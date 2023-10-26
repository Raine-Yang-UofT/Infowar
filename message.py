from dataclasses import dataclass
from typing import Any


@dataclass
class Message:
    """
    A message from client

    Representation invariables:
        source: the id of the player who sends message
        type: the type of message
        command: the specific command player sends
        data: any data in the message (if required)
        priority: the order of message in message queue,
                  lower value for higher priority
    """
    source: int
    type: int
    command: int
    data: Any
    priority: int

    def __lt__(self, other):
        """
        Override the comparison between messages

        :param other: another Message instance
        :return: whether this message has a higher priority
        """
        return self.priority < other.priority


"""
Defining Directions
"""
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

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
MOVE = 100
