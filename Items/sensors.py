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


@dataclass
class Lidar:
    """
    Detect a square range around player and update the map

    Representation invariants:
        - name: the name of sensor
        - radius: the detection radius
        - sound_emission: the sound emission of the sensor
        - heat_emission: the heat emission of the sensor
        - message: the message associated with the sensor
    """
    name: str
    radius: int
    sound_emission: int
    heat_emission: int
    message: int
