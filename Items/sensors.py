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


@dataclass
class Drone:
    """
    Move to a certain location based on player's command
    and detect a square region around the location

    Representation invariants:
        - name: the name of sensor
        - radius: the detection radius
        - sound_emission: the sound emission of the sensor
        - heat_emission: the heat emission of the sensor
        - message: the message associated with the sensor
        - commands: the commands inputed by player
        - longest_range: the longest path the drone can move (maximum command length)
        - location: the final location of the drone
    """
    name: str
    radius: int
    sound_emission: int
    heat_emission: int
    message: int
    commands: str
    longest_range: int
    location: tuple[int, int]


@dataclass
class ScoutCar:
    """
    Move to a certain location based on player's command
    and detect a square region around the location
    can be blocked by barricades

    Representation invariants:
        - name: the name of sensor
        - radius: the detection radius
        - sound_emission: the sound emission of the sensor
        - heat_emission: the heat emission of the sensor
        - message: the message associated with the sensor
        - direction: the direction of cat movement
        - location: the final location of the drone
        - max_barricade_remove: the maximum number of barricades the scout car can remove
    """
    name: str
    radius: int
    sound_emission: int
    heat_emission: int
    message: int
    direction: str
    location: tuple[int, int]
    max_barricade_remove: int
