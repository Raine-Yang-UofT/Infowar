from dataclasses import dataclass
import damage as dmg


@dataclass(frozen=True)
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


@dataclass(frozen=True)
class ProjectileWeapon:
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
        - message: the message related to weapon (direction, range)
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
    message: tuple[int, int]

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


# weapons
assulter_rifle = StraightWeapon("assulter rifle", dmg.Damage(80, 3), 0.75, 0.03, 8, 6, 4, 40, 0)
submachine_gun = StraightWeapon("submachine gun", dmg.Damage(70, 2), 0.9, 0.03, 6, 5, 3, 65, 0)
pistol = StraightWeapon("pistol", dmg.Damage(60, 2), 0.95, 0.02, 5, 4, 2, 90, 0)
sniper_rifle = StraightWeapon("sniper_rifle", dmg.Damage(100, 4), 0.2, -0.03, 12, 8, 5, 10, 0)
shotgun = StraightWeapon("shotgun", dmg.Damage(100, 1), 1, 0.15, 4, 7, 4, 30, 0)

# projectile weapons
impact_grenade = ProjectileWeapon("impact grenade", dmg.Damage(40, 0), 4, 6, 3, 10, 4, 2, 60, (0, 0))
frag_grenade = ProjectileWeapon("frag grenade", dmg.Damage(60, 2), 3, 6, 2, 20, 5, 3, 30, (0, 0))
breaching_grenade = ProjectileWeapon("breaching grenade", dmg.Damage(10, 5), 3, 5, 2, 0, 5, 2, 80, (0, 0))
