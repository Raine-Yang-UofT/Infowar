"""
The class for a player-controlled robot
"""
from Framework.interface import IDisplayable, IDamageable
from damage import Damage
from Configurations.robot_config import RobotConfig
from grid import Grid
import Configurations.game_config as game_config
import random
from dataclasses import dataclass


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
            if element != '*':
                print(element, end="  ")
                contains_valid_data = True
        if contains_valid_data:
            print()


@dataclass
class RobotState:
    """
    the class for robot states

        - vision: whether the robot has vision
        - move: whether the robot can move
        - sensor: whether the robot can use sensors
        - weapon: whether the robot can use weapons
        - gadget: whether the robot can use gadgets
        - alive: whether the robot is alive
    """
    vision: bool
    move: bool
    sensor: bool
    weapon: bool
    gadget: bool
    alive: bool

    def set_normal(self):
        """
        set the robot to normal state

        :return: None
        """
        self.vision = True
        self.move = True
        self.sensor = True
        self.weapon = True
        self.gadget = True
        self.alive = True

    def set_dead(self):
        """
        set the robot to dead state

        :return: None
        """
        self.vision = False
        self.move = False
        self.sensor = False
        self.weapon = False
        self.gadget = False
        self.alive = False

    def set_state(self, vision: bool = None, move: bool = None, sensor: bool = None, weapon: bool = None, gadget: bool = None, alive: bool = None):
        """
        set the robot to a given state

        :param vision: whether the robot has vision
        :param move: whether the robot can move
        :param sensor: whether the robot can use sensors
        :param weapon: whether the robot can use weapons
        :param gadget: whether the robot can use gadgets
        :param alive: whether the robot is alive
        :return: None
        """
        self.vision = vision if vision is not None else self.vision
        self.move = move if move is not None else self.move
        self.sensor = sensor if sensor is not None else self.sensor
        self.weapon = weapon if weapon is not None else self.weapon
        self.gadget = gadget if gadget is not None else self.gadget
        self.alive = alive if alive is not None else self.alive


class Robot(IDisplayable, IDamageable):

    def __init__(self, robot_config: RobotConfig, player_id: int) -> None:
        """
        initialize the robot and its sensors and weapons

        :param robot_config: config file for robot
        :param player_id: the id assigned by server
        """
        # the id assigned to player and game
        self.player_id = player_id
        self.state = RobotState(True, True, True, True, True, True)

        # extract base configuration
        self.max_HP = robot_config.HP
        self.armor_equip = robot_config.armor
        self.move_sound = robot_config.move_sound
        self.move_heat = robot_config.move_heat
        self.move_speed = robot_config.move_speed

        # the robot current status: initialize as max values
        self.HP = self.max_HP
        self.armor = self.armor_equip.max_armor

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
        self.map = [["*" for _ in range(0, game_config.FIELD_COL)] for _ in range(0, game_config.FIELD_ROW)]
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
        status_message = "Player " + str(self.player_id) + "  HP: " + str(self.HP) + '/' + str(self.max_HP) + "  armor: " + str(self.armor) + '/' + str(self.armor_equip.max_armor)
        return status_message

    def get_id(self) -> int:
        """
        Return player_id of the robot

        :return: self.player_id
        """
        return self.player_id

    def get_name(self) -> str:
        """
        Return the name of the robot

        :return: the name of robot
        """
        return 'player ' + str(self.player_id)

    def get_state(self) -> RobotState:
        """
        Return the state of robot

        :return: self.state
        """
        return self.state

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
                # print_sensor_helper(info)
                print_list_helper(info)
            else:
                print('Unrecognized information type')

    def clear_info(self) -> None:
        """
        Clear the list self.info_list

        :return: None
        """
        self.info_list.clear()

    def update_map(self, robot_vision: list[list[str]]) -> None:
        """
        Update the player's local map

        :param robot_vision: the field of vision obtained by player
        :return: None
        """
        for i in range(0, len(robot_vision)):
            for j in range(0, len(robot_vision[0])):
                if self.map[i][j] != robot_vision[i][j] and robot_vision[i][j] != '*':
                    self.map[i][j] = robot_vision[i][j]
                    # hide enemy robots
                    if robot_vision[i][j] == 'R' and (j, i) != self.grid.get_pos():
                        self.map[i][j] = '_'

    def update_vision(self, robot_vision: list[list[str]]) -> None:
        """
        Update the player's vision

        :param robot_vision: the field of vision obtained by player
        :return: None
        """
        # check robot state
        if not self.get_state().vision:
            self.receive_info("Robot vision is interrupted!")
            return

        x, y = self.grid.get_pos()
        for i in range(y - 1, y + 2):
            row = []
            for j in range(x - 1, x + 2):
                if i < 0 or i >= len(robot_vision) or j < 0 or j >= len(robot_vision):
                    row.append('*')
                else:
                    row.append(robot_vision[i][j])
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

    def get_damage(self, damage: Damage):
        """
        Receive damage. Override get_damage() in IDamageable

        :param damage: the damage information
        :return: None
        """
        if self.armor >= damage.penetration:    # armor blocks part of damage
            self.HP -= int(damage.damage * (1 - self.armor_equip.armor_protection))
            # check if armor decreases
            if random.random() <= self.armor_equip.armor_reduction_rate:
                self.armor = max(0, self.armor - 1)
        else:   # armor is penetrated
            self.HP -= damage.damage

        self.receive_info("Receives damage!")

        if self.HP <= 0:
            self.state.set_dead()  # change robot state to dead
            self.receive_info("Robot destroyed!")
