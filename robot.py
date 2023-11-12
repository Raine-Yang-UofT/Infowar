"""
The class for a player-controlled robot
"""
from interface import IDisplayable, IDamageable
from Configurations.robot_config import RobotConfig
from grid import Grid
from Configurations.game_config import FIELD_ROW, FIELD_COL


def print_list_helper(lst: list[list]) -> None:
    """
    Helper function, print a 2D list

    :return: None
    """
    for row in lst:
        for element in row:
            print(element, end="  ")
        print()


def print_sensor_helper(reading: list[list]) -> None:
    """
    Helper function, print a 2D list for sensor data
    Omit blank spaces in the list

    :return: None
    """
    for row in reading:
        contains_valid_data = False  # check if the list is not all blank blocks
        for element in row:
            if element != ' ':
                print(element, end="  ")
                contains_valid_data = True
        if contains_valid_data:
            print()


class Robot(IDisplayable, IDamageable):

    def __init__(self, robot_config: RobotConfig, player_id: int) -> None:
        """
        initialize the robot and its sensors and weapons

        :param robot_config: config file for robot
        :param player_id: the id assigned by server
        """
        # the id assigned to player and game
        self.player_id = player_id

        # extract base configuration
        self.max_HP = robot_config.HP
        self.max_armor = robot_config.armor
        self.move_sound = robot_config.move_sound
        self.move_heat = robot_config.move_heat
        self.move_speed = robot_config.move_speed

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
        # the robot's information list
        self.info_list = []
        # the robot's local map
        self.map = [[" " for _ in range(0, FIELD_COL)] for _ in range(0, FIELD_ROW)]
        # the robot's current vision
        self.vision = []

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
        If the information is a string, print it directly
        If the information is a list, print it with print_list_helper

        :return: None
        """
        for info in self.info_list:
            if isinstance(info, str):
                print(info)
            elif isinstance(info, list):
                print_sensor_helper(info)
            else:
                print('Unrecognized information type')

    def clear_info(self) -> None:
        """
        Clear the list self.info_list

        :return: None
        """
        self.info_list.clear()

    def update_map(self, vision: list[list[str]]) -> None:
        """
        Update the player's local map

        :param vision: the field of vision obtained by player
        :return: None
        """
        for i in range(0, len(vision)):
            for j in range(0, len(vision[0])):
                if self.map[i][j] != vision[i][j] and vision[i][j] != ' ':
                    self.map[i][j] = vision[i][j]
                    # hide enemy robots
                    if vision[i][j] == 'R' and (j, i) != self.grid.get_pos():
                        self.map[i][j] = '_'

    def update_vision(self, vision: list[list[str]]) -> None:
        """
        Update the player's vision

        :param vision: the field of vision obtained by player
        :return: None
        """
        x, y = self.grid.get_pos()
        for i in range(y - 1, y + 2):
            row = []
            for j in range(x - 1, x + 2):
                if i < 0 or i >= len(vision) or j < 0 or j >= len(vision):
                    row.append('*')
                else:
                    row.append(vision[i][j])
            self.vision.append(row)

    def print_vision(self) -> None:
        """
        Print vision to console

        :return: None
        """
        print_list_helper(self.vision)

    def print_map(self) -> None:
        """
        Print the local map to console

        :return: None
        """
        print_list_helper(self.map)
