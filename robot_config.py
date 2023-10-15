"""
The configurations for robots, sensors, weapons, and gadgets
"""
from dataclasses import dataclass


@dataclass
class SensorConfig:
    """
    configurations for sensors
    """
    pass


@dataclass
class WeaponConfig:
    """
    configurations for weapons
    """
    pass


@dataclass
class GadgetConfig:
    """
    configurations for gadgets
    """
    pass


class RobotConfig:
    """
    configurations for robot
    """
    def __init__(self, HP: int, armor: int) -> None:
        self.HP = HP
        self.armor = armor
        # TODO: add configurations of sensors, weapons, and gadgets
        self.sensors = None
        self.weapons = None
        self.gadgets = None
