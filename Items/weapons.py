from dataclasses import dataclass
import damage as dmg


@dataclass
class StraightWeapon:
    """
    Configurations for straight-firing weapons

        - name: the name of weapon
        - damage: the damage information
        - accuracy: the accuracy of the weapon
        - accuracy_decay: the decay of accuracy through distance
        - range: the range of weapon
        - sound_emission: the sound emission of the weapon
        - heat_emission: the heat emission of the weapon
        - reaction_time: the reaction speed of weapon (determines message priority)
        - message: the message related to weapon
    """
    name: str
    damage: dmg.Damage
    accuracy: float
    accuracy_decay: float
    range: int
    sound_emission: int
    heat_emission: int
    reaction_time: int
    message: int


# weapons
assulter_rifle = StraightWeapon("assulter rifle", dmg.Damage(80, 3), 0.75, 0.03, 8, 6, 4, 40, 0)
submachine_gun = StraightWeapon("submachine gun", dmg.Damage(70, 2), 0.85, 0.02, 6, 5, 3, 65, 0)
pistol = StraightWeapon("pistol", dmg.Damage(50, 2), 0.95, 0.02, 5, 4, 2, 90, 0)
sniper_rifle = StraightWeapon("sniper_rifle", dmg.Damage(90, 4), 0.2, -0.05, 12, 8, 5, 20, 0)
shotgun = StraightWeapon("shotgun", dmg.Damage(100, 0), 1, 0.1, 4, 7, 4, 30, 0)
