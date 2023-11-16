from dataclasses import dataclass


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
