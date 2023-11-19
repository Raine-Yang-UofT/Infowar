from dataclasses import dataclass


@dataclass
class Damage:
    """
    The damage information

        - damage: the damage value
        - penetration: the penetration of damage
    """
    damage: int
    penetration: int
