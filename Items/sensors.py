"""
Sensor items
"""

from dataclasses import dataclass


@dataclass
class SignalSensor:
    """
    Detect signal at a square region with a given radius around player

    Representation invariants:
        - name: the name of sensor
        - radius: the detection radius
        - message: the message associated with the sensor
    """
    name: str
    radius: int
    message: int
