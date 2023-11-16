from dataclasses import dataclass
import damage as dmg


@dataclass
class StraightWeapon:
    """
    Configurations for straight-firing weapons

    Representation invariants:
        - damage: the damage information
        - sound_emission: the sound emission of the weapon
        - heat_emission: the heat emission of the weapon
        - reaction: the reaction speed of weapon (determines message priority)
    """
    damage: dmg.StraightDamage
    sound_emission: int
    heat_emission: int
    reaction: int


# weapons
assulter_rifle = StraightWeapon(dmg.StraightDamage(75, 3, 0.75, 0.06, 8), 6, 4, 40)
submachine_gun = StraightWeapon(dmg.StraightDamage(60, 2, 0.9, 0.05, 6), 5, 3, 65)
pistol = StraightWeapon(dmg.StraightDamage(30, 2, 0.95, 0.02, 4), 4, 2, 90)
sniper_rifle = StraightWeapon(dmg.StraightDamage(80, 4, 0.2, -0.05, 12), 8, 5, 20)
shotgun = StraightWeapon(dmg.StraightDamage(100, 0, 1, 0.2, 4), 7, 4, 30)
