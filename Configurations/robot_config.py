"""
The configurations for robots, sensors, weapons, and gadgets
"""
from dataclasses import dataclass

@dataclass
class BaseConfig:
    """
    configurations for robot base

    Representative invariables:
        -HP: the robot's HP
        -armor: the robot's armor
        -move_sound: the sound generated when robot moves
        -move_heat: the heat generated when robot moves
    """
    HP: int
    armor: int
    move_sound: int
    move_heat: int

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
    def __init__(self, base: BaseConfig) -> None:
        self.base = base
        # TODO: add configurations of sensors, weapons, and gadgets
        self.sensors = None
        self.weapons = None
        self.gadgets = None


# a default configuration for testing
default_base = BaseConfig(
    HP=100,
    armor=3,
    move_sound=5,
    move_heat=3
)
