"""
The class for a player-controlled robot
"""
from interface import IDisplayable, IDamageable
from robot_config import RobotConfig, BaseConfig, SensorConfig, WeaponConfig, GadgetConfig
from grid import Grid


class Robot(IDisplayable, IDamageable):

    def __init__(self, robot_config: RobotConfig, player_id: int) -> None:
        """
        initialize the robot and its sensors and weapons

        :param robot_config: config file for robot
        :param player_id: the id assigned by server
        """
        # extract configurations from RobotConfig
        base = robot_config.base

        # the id assigned to player and game
        self.player_id = player_id

        # extract base configuration
        self.max_HP = base.HP
        self.max_armor = base.armor
        self.move_sound = base.move_sound
        self.move_heat = base.move_heat

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
        self.grid = None
        # the robot's local map
        self.map = []
        # the robot's information list
        self.info_list = []

    def display(self) -> str:
        """
        override the method in IDisplayable, display a robot as 'R'

        :return: 'R'
        """
        return 'R'

    def display_status(self) -> str:
        """
        Display the status of robot in string

        :return: a string containing status information
        """
        status_message = "Player " + str(self.player_id) + "  HP: " + str(self.HP) + '/' + str(self.max_HP) + "  armor: " + str(self.armor) + '/' + str(self.max_armor)
        return status_message

    def get_id(self) -> int:
        """
        Return player_id of the robot

        :return: self.player_id
        """
        return self.player_id

    def set_pos(self, grid: Grid) -> None:
        """
        Set the grid where the robot occupies

        :param grid: the grid to place the robot
        :return: None
        """
        self.grid = grid

    def get_pos(self):
        """
        Return the (row, col) of the grid the robot is in
        Return None if the robot's grid is not assigned

        :return: the (row, col) of self.grid, None if self.grid is not assigend
        """
        if self.grid is None:
            return None

        return self.grid.get_pos()

    def receive_info(self, info: str) -> None:
        """
        Add one line of information for display
        in the robot's info_list

        :param info: the line of information
        :return: None
        """
        self.info_list.append(info)

    def print_info(self) -> None:
        """
        Print all information gathered from self.info_list to console
        and clear the list

        :return: None
        """
        for info in self.info_list:
            print(info)

        self.info_list.clear()
