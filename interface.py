"""
A Module containing all interface definitions
"""
from dataclasses import dataclass
import damage as dmg


class IDisplayable:
    """
    IDisplayable: an object can be displayed as a string representation

    child classes should implement display() method
    """
    def display(self) -> str:
        """
        Return a string display of the obejct

        :return: the object's string representation
        """
        # Override in children class


class IDamageable:
    """
    IDamageable: an object can be damaged by weapons

    child classes should implement get_damage() method
    """
    def get_damage(self, damage: dmg.Damage):
        """
        Impose certain damage on the object with a given damage and penetration

        :param damage: the damage
        :return: None
        """
        # Override in children class

