"""
The battlefield in the game, consisting a 2D list of grids
"""
import random
import math

from grid import Grid
from Framework.interface import IDisplayable
from barricade import Barricade
from barricade import HardBarricade
from robot import Robot


class Battlefield(IDisplayable):

    def __init__(self, rows: int, columns: int) -> None:
        """
        Create a new empty 2D list consisting of empty Grid

        :param rows: the num of rows in the battlefield
        :param columns: the num of colomns in the battlefield
        """
        # create new empty grid
        self.field = [[Grid((j, i)) for j in range(0, columns)] for i in range(0, rows)]

    def initialize_field(self, barricade_coverage: float, hard_barricade_coverage: float,
                         barricade_HP_range: tuple, barricade_armor_range: tuple) -> None:
        """
        Install barricades and hard barricades at random locations on the field

        Preconditions:
            - 0 <= barricade_coverage < 1
            - 0 <= hard_barricade_coverage < barricade_coverage
            - len(barricade_HP_range) == 2 and barricade_HP_range[1] >= barricade_HP_range[0]
            - len(barricade_armor_range) == 2 and barricade_armor_range[1] >= barricade_armor_range[0]

        :param barricade_coverage: the proportion of field covered by barricade
        :param hard_barricade_coverage: the proportion of field covered by hard_barricade,
                                        hard barricades are covered on barricade
        :param barricade_HP_range: the range of HP for hard barricade
        :param barricade_armor_range: the range of armor for hard barricade
        :return: None
        """
        for row in self.field:
            for grid in row:
                random_temp = random.random()
                set_barricade = random_temp <= barricade_coverage
                set_hard_barricade = random_temp <= hard_barricade_coverage
                if not grid.get_occupant() and set_barricade:  # cover an empty grid
                    if set_hard_barricade:
                        # set up hard barricade with random HP and armor in range
                        HP_range = random.randint(barricade_HP_range[0], barricade_HP_range[1])
                        armor_range = random.randint(barricade_armor_range[0], barricade_armor_range[1])
                        grid.change_occupant(HardBarricade(HP_range, armor_range, grid))
                    else:
                        # set up barricade
                        grid.change_occupant(Barricade(grid))

    def initialize_player_location(self, player: Robot, max_trial=20):
        """
        Spawn the player at random empty locations on the field.
        If an empty location is not found in max_trail times, spawn at any location not occupied by another player

        :param player: the player to place
        :param max_trial: the maximum times to select empty locations before overriding an existing barricade is allowed
        :return: None
        """
        fixed = False  # whether a valid location is selected
        trail = 0
        while not fixed:
            trail += 1
            row = random.randint(0, len(self.field) - 1)
            col = random.randint(0, len(self.field[0]) - 1)
            grid = self.field[row][col]
            if grid.get_occupant() is None:  # find empty grid
                grid.change_occupant(player)
                player.set_pos(grid)
                fixed = True
            elif not isinstance(grid.get_occupant(), Robot) and trail > max_trial:  # not override another player
                grid.change_occupant(player)
                player.set_pos(grid)
                fixed = True

    def get_grid(self, x: int, y: int):
        """
        Return the grid at a given row and col, return none if the
        indexes are out of bound

        :param x: the x-coordinate of grid
        :param y: the y-ccordinate of grid
        :return: field[y][x]
        """
        if y < 0 or y >= len(self.field) or x < 0 or x >= len(self.field[0]):
            print("grid index out of bound")
            return None

        return self.field[y][x]

    def is_blocked(self, x: int, y: int) -> bool:
        """
        Return whether field[row][col] is occupied by a player
        or a hard barricade

        Return True if (x, y) is out of bound

        :param x: the x-coordinate of grid
        :param y: the y-ccordinate of grid
        :return: whether the grid is blocked
        """
        # check out-of-bound cases
        if self.get_grid(x, y) is None:
            return True

        return self.get_grid(x, y).display() == '#' or self.get_grid(x, y).display() == 'R'

    def is_occupied(self, x: int, y: int) -> bool:
        """
        Return whether field[row][col] is occupied by any object

        Return True if (x. y) is out of bound

        :param x: the x-coordinate of grid
        :param y: the y-ccordinate of grid
        :return: whether the grid is occupied
        """
        if self.get_grid(x, y) is None:
            return True

        return not self.get_grid(x, y).display() == '_'

    def generate_heat(self, x: int, y: int, intensity: int) -> None:
        """
        Generate heat signal from a given coordinate (x, y)

        Preconditions:
            - 0 <= x < len(self.field[0])
            - 0 <= y < len(self.field)

        :param x: the x-coordinate of the heat source
        :param y: the y-coordinate of the heat source
        :param intensity: the intensity of the heat
        :return: None
        """
        for field_row in self.field:
            for grid in field_row:
                px, py = grid.get_pos()
                grid.change_heat(max(intensity - int(math.sqrt((x - px) ** 2 + (y - py) ** 2)), 0))

    def generate_sound(self, x: int, y: int, intensity: int) -> None:
        """
        Generate sound signal from a given coordinate (x, y)

        Preconditions:
            - 0 <= x < len(self.field[0])
            - 0 <= y < len(self.field)

        :param x: the x-coordinate of the sound source
        :param y: the y-coordinate of the sound source
        :param intensity: the intensity of the sound
        :return: None
        """
        for field_row in self.field:
            for grid in field_row:
                px, py = grid.get_pos()
                grid.change_sound(max(intensity - int(math.sqrt((x - px) ** 2 + (y - py) ** 2)), 0))

    def reduce_sound_and_heat(self, sound_reduction: int, heat_reduction: int) -> None:
        """
        Reduce the sound and heat intensity in the entire field

        Preconditions:
            - sound_reduction >= 0
            - heat_reduction >= 0

        :param sound_reduction: the amount of sound reduced
        :param heat_reduction: the amount of heat reduced
        :return: None
        """
        for field_row in self.field:
            for grid in field_row:
                grid.change_sound(-sound_reduction)
                grid.change_heat(-heat_reduction)

    def display(self) -> list[list[str]]:
        """
        Override display() in IDisplayable

        :return: a string representation of the battlefield
        """
        return [[grid.display() for grid in row] for row in self.field]
