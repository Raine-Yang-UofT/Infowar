"""
The class for a player-controlled robot
"""
from interface import IDisplayable, IDamageable
from robot_config import RobotConfig
from grid import Grid


class Robot(IDisplayable, IDamageable):

    def __init__(self, robot_config: RobotConfig, player_id: int) -> None:
        """
        initialize the robot and its sensors and weapons

        :param robot_config: config file for robot
        :param player_id: the id assigned by server
        """
        # the id assigned to player
        self.player_id = player_id

        # the robot configurations
        self.max_HP = robot_config.HP
        self.max_armor = robot_config.armor

        # the robot current status: initialize as max values
        self.HP = self.max_HP
        self.armor = self.max_armor

        # the sensor configurations
        self.sensors = robot_config.sensors
        # the weapon configurations
        self.weapons = robot_config.weapons
        # the gadget configurations
        self.gadgets = robot_config.gadgets

        # position initialized by server
        self.pos = None

    def display(self) -> str:
        """
        override the method in IDisplayable, display a robot as 'R'

        :return: 'R'
        """
        return 'R'

    def get_id(self) -> int:
        """
        Return player_id of the robot

        :return: self.player_id
        """
        return self.player_id

    def set_position(self, grid: Grid) -> None:
        """
        Set the grid where the robot occupies

        :param grid: the grid to place the robot
        :return: None
        """
        self.pos = grid

    def move(self, direction):
        """
        move the robot on the map

        :param: direction: the movement direction
        :return: None
        """




