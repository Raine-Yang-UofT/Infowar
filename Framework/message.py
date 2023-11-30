from dataclasses import dataclass, field
from typing import Any


@dataclass(order=True)
class Message:
    """
    A message from client

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
TYPE_DISCONNECT = 2
TYPE_MOVE = 10
TYPE_FIRE = 11
TYPE_SENSE = 12
TYPE_GADGET = 13

"""
Message Commands
"""
CONNECT = 1
DISCONNECT = 2
MOVE = 100
# sensor message
SENSE_SOUND = 200
SENSE_HEAT = 201
SENSE_LIDAR = 202
SENSE_DRONE = 203
SENSE_SCOUT_CAR = 204
