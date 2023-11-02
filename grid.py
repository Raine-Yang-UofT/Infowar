"""
A single grid in the game map
"""
import interface


class Grid:

    def __init__(self, pos: tuple) -> None:
        """
        Initialize the heat, sound, and occupant of the grid

        :param pos: the x and y coordinates of the grid
        """
        self.heat = 0
        self.sound = 0
        self.occupant = None
        self.pos = pos

    def get_pos(self) -> tuple:
        """
        Return the grid's position in field

        :return: (x, y) of the grid's position
        """
        return self.pos

    def change_heat(self, value: int) -> None:
        """
        Change the heat of the grid, the final heat is between 0 and 9

        :param value: the change in heat
        :return: None
        """
        final_heat = self.heat + value
        # constrain heat between 0 and 9
        self.heat = max(min(final_heat, 9), 0)

    def change_sound(self, value: int) -> None:
        """
        Change the sound of the grid, the final heat is between 0 and 9

        :param value: the change in sound
        :return: None
        """
        final_sound = self.sound + value
        # constrain heat between 0 and 9
        self.sound = max(min(final_sound, 9), 0)

    def change_occupant(self, occupant: interface.IDisplayable) -> None:
        """
        Add an occupant to the grid

        To remove the occupant in the grid, pass None as occupant

        :param occupant: the occupant added on the grid
        :return: None
        """
        self.occupant = occupant

    def get_sound(self) -> int:
        """
        :return: the sound in grid
        """
        return self.sound

    def get_heat(self) -> int:
        """
        :return: the sound in grid
        """
        return self.heat

    def get_occupant(self) -> interface.IDisplayable:
        """
        :return: the sound in grid
        """
        return self.occupant

    def remove_occupant(self) -> None:
        """
        clear the occupant in the grid

        :return: None
        """
        self.occupant = None

    def display(self) -> str:
        """
        Show a string representation of the occupant of the grid

        '_': empty grid
        'R': robot
        '#': hard barricade
        'x': barricade

        Invoke the 'display' method for IDisplayable objects

        :return: the string for occupant
        """
        if not self.occupant:   # the occupant is None
            return '_'
        else:
            return self.occupant.display()

