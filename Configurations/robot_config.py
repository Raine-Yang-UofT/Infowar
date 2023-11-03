"""
The configurations for robots, sensors, weapons, and gadgets
"""
from dataclasses import dataclass


@dataclass
class RobotConfig:
    """
    configurations for robot

    Representative invariables:
        -HP: the robot's HP
        -armor: the robot's armor
        -move_sound: the sound generated when robot moves
        -move_heat: the heat generated when robot moves
        -sensors: the sensors equipped
        -weapons: the weapons equipped
        -gadgets: the gadgets equipped
    """
    HP: int
    armor: int
    move_sound: int
    move_heat: int
    sensors: list
    weapons: list
    gadgets: list


# a default configuration for testing
default_config = RobotConfig(
    HP=100,
    armor=3,
    move_sound=5,
    move_heat=3,
    sensors=[],
    weapons=[],
    gadgets=[]
)
