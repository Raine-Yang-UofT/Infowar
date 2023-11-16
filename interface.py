"""
A Module containing all interface definitions
"""
from dataclasses import dataclass


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


@dataclass
class Damage:
    """
    The damage information

    Representation invariants:
        - damage: the damage value
        - penetration: the penetration of damage
    """
    damage: int
    penetration: int


@dataclass
class StraightDamage(Damage):
    """
    The damage information for straight weapons

    Representation invariants:
        - damage: the damage value
        - penetration: the penetration of damage
        - accuracy: the accuracy of the weapon
        - accuracy_decay: the decay of accuracy through distance
        - range: the range of weapon
    """
    damage: int
    penetration: int
    accuracy: float
    accuracy_decay: float
    range: int


class IDamageable:
    """
    IDamageable: an object can be damaged by weapons

    child classes should implement get_damage() method
    """
    def get_damage(self, damage: Damage):
        """
        Impose certain damage on the object with a given damage and penetration

        :param damage: the damage
        :return: None
        """
        # Override in children class

