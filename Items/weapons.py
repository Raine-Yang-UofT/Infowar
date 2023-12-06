from dataclasses import dataclass
import damage as dmg
from Framework import interface
from Items import prompt_template as prompt


@dataclass(frozen=True)
class StraightWeaponConfig:
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
    """
    name: str
    damage: dmg.Damage
    accuracy: float
    accuracy_decay: float
    range: int
    sound_emission: int
    heat_emission: int
    reaction_time: int


class StraightWeapon(interface.IWeapon):
    """
    The straight-firing weapon class
    """
    def __init__(self, config: StraightWeaponConfig):
        self.config = config
        self.direction = -1   # the direction of firing

    def fire_weapon(self, weapons, robot) -> None:
        """
        Fire straight weapons from robot

        :param weapons: the RobotWeapons observer class
        :param robot: the robot that fires the weapon
        :return: None
        """
        result = weapons.shoot_straight_weapon(robot.get_pos()[0], robot.get_pos()[1], self)
        if result is not None:
            robot.receive_info(result)

    def select_weapon_parameter(self):
        """
        Add additional parameters to weapon

        :return: a copy of weapon object with updated parameters
        """
        return prompt.select_direction(self, "Select the direction of firing:")


@dataclass(frozen=True)
class ProjectileWeaponConfig:
    """
    Configurations for projectile weapons

        - name: the name of weapon
        - damage: the damage information
        - min_launch_range: the minimum range to launch weapon
        - max_launch_range: the maximum range to launch weapon
        - impact_radius: the impact radius (circular) of weapon
        - impact_damage_decay: the damage decay through impact range
        - sound_emission: the sound emission of the weapon
        - heat_emission: the heat emission of the weapon
        - reaction_time: the reaction speed of weapon (determines message priority)
    """
    name: str
    damage: dmg.Damage
    min_launch_range: int
    max_launch_range: int
    impact_radius: int
    impact_damage_decay: int
    sound_emission: int
    heat_emission: int
    reaction_time: int


class ProjectileWeapon(interface.IWeapon):
    """
    The projectile weapon class
    """
    def __init__(self, config: ProjectileWeaponConfig):
        self.config = config
        # the direction and range of firing
        self.direction = -1
        self.range = -1

    def fire_weapon(self, weapons, robot) -> None:
        """
        Fire projectile weapons from robot

        :param weapons: the RobotWeapons observer class
        :param robot: the robot that fires the weapon
        :return: None
        """
        results = weapons.shoot_projectile_weapon(robot.get_pos()[0], robot.get_pos()[1], self)
        if results is not None:
            for info in results:
                robot.receive_info(info)

    def select_weapon_parameter(self):
        """
        Add additional parameters to weapon

        :return: a copy of weapon object with updated parameters
        """
        return prompt.select_direction_and_range(self, "Select the direction of firing:", "Select the range of firing:")


# weapons
assulter_rifle = StraightWeapon(
    StraightWeaponConfig(
        name="assulter rifle",
        damage=dmg.Damage(80, 3),
        accuracy=0.75,
        accuracy_decay=0.03,
        range=8,
        sound_emission=6,
        heat_emission=4,
        reaction_time=40
    )
)

submachine_gun = StraightWeapon(
    StraightWeaponConfig(
        name="submachine gun",
        damage=dmg.Damage(70, 2),
        accuracy=0.85,
        accuracy_decay=0.03,
        range=6,
        sound_emission=5,
        heat_emission=3,
        reaction_time=65
    )
)

pistol = StraightWeapon(
    StraightWeaponConfig(
        name="pistol",
        damage=dmg.Damage(60, 2),
        accuracy=0.95,
        accuracy_decay=0.02,
        range=5,
        sound_emission=4,
        heat_emission=2,
        reaction_time=90
    )
)

sniper_rifle = StraightWeapon(
    StraightWeaponConfig(
        name="sniper_rifle",
        damage=dmg.Damage(100, 4),
        accuracy=0.2,
        accuracy_decay=-0.03,
        range=12,
        sound_emission=6,
        heat_emission=5,
        reaction_time=10
    )
)

shotgun = StraightWeapon(
    StraightWeaponConfig(
        name="shotgun",
        damage=dmg.Damage(100, 1),
        accuracy=1,
        accuracy_decay=0.15,
        range=4,
        sound_emission=7,
        heat_emission=4,
        reaction_time=30
    )
)

# projectile weapons
impact_grenade = ProjectileWeapon(
    ProjectileWeaponConfig(
        name="impact grenade",
        damage=dmg.Damage(40, 1),
        min_launch_range=4,
        max_launch_range=6,
        impact_radius=3,
        impact_damage_decay=10,
        sound_emission=4,
        heat_emission=2,
        reaction_time=60
    )
)

frag_grenade = ProjectileWeapon(
    ProjectileWeaponConfig(
        name="frag grenade",
        damage=dmg.Damage(60, 2),
        min_launch_range=3,
        max_launch_range=6,
        impact_radius=2,
        impact_damage_decay=20,
        sound_emission=5,
        heat_emission=3,
        reaction_time=30
    )
)

breaching_grenade = ProjectileWeapon(
    ProjectileWeaponConfig(
        name="breaching grenade",
        damage=dmg.Damage(5, 5),
        min_launch_range=3,
        max_launch_range=5,
        impact_radius=2,
        impact_damage_decay=0,
        sound_emission=5,
        heat_emission=2,
        reaction_time=20
    )
)
