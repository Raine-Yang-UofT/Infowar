"""
Class definitions for barricade and hard barricade

A barricade is an obstacle that occupies a grid. A barricade can block one
weapon shot and be destroyed. A barricade is also destroyed when a player
moves to the same grid it occupies

A hard barricade has a certain HP and is destroeyd only when it loses all
HP from weapon shot. Player cannot move to a grid occupied by a hard barricade
"""
from Framework.interface import IDisplayable, IDamageable
from damage import Damage
from grid import Grid


class Barricade(IDisplayable, IDamageable):

    def __init__(self, grid: Grid) -> None:
        self.grid = grid

    def display(self) -> str:
        """
        Override display() method in IDisplayable

        :return: 'x': representation of barricade
        """
        return 'x'

    def get_damage(self, damage: Damage):
        """
        Override get_damage() method in IDamageable

        eliminate the barricade when receive damage
        """
        self.grid.remove_occupant()  # erase the barricade

    def get_name(self) -> str:
        """
        Return the name of the barricade

        :return: 'barricade'
        """
        return 'barricade'


class HardBarricade(IDisplayable, IDamageable):

    def __init__(self, hp: int, armor: int, grid: Grid) -> None:
        self.HP = hp
        self.armor = armor
        self.grid = grid

    def display(self) -> str:
        """
        Override display() method in IDisplayable

        :return: '#': representation of hard barricade
        """
        return '#'

    def get_damage(self, damage: Damage):
        """
        Override get_damage() method in IDamageable

        If penetration is larger than self.armor, the hard barricade is immediately destroyed
        Otherwise, self.HP reduces the value of damage. The hard barricade is destroyed when
        HP is lower than 0
        """
        if damage.penetration >= self.armor:
            self.grid.remove_occupant()  # erase the hard barricade
        else:
            self.HP -= damage.damage
            if self.HP <= 0:
                self.grid.remove_occupant()  # erase the hard barricade

    def get_name(self) -> str:
        """
        Return the name of the barricade

        :return: 'hard barricade'
        """
        return 'hard barricade'
