from dataclasses import dataclass
import damage as dmg
from Framework import interface
from Framework import input_code


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
        self.message = -1   # the direction of firing

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
        command_input = input("Select the direction of firing:" +
                              input_code.UP + ": up  " + input_code.DOWN + ": down  " + input_code.LEFT + ": left  " + input_code.RIGHT + ": right")
        if command_input not in [input_code.UP, input_code.DOWN, input_code.LEFT, input_code.RIGHT]:
            raise input_code.InvalidCommandException()
        self.message = input_code.get_direction_message(command_input)  # update weapon message as firing direction
        return self


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
        self.message = (-1, -1)     # the direction and range of firing

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
        command_input = input("Select the direction of firing:" +
                              input_code.UP + ": up  " + input_code.DOWN + ": down  " + input_code.LEFT + ": left  " + input_code.RIGHT + ": right")
        range_input = input("Select the range of firing: (range between " + str(self.config.min_launch_range) + " - " + str(self.config.max_launch_range) + ")")
        if range_input.isdigit():
            range_input = int(range_input)
        else:
            raise input_code.InvalidCommandException()

        if ((command_input not in [input_code.UP, input_code.DOWN, input_code.LEFT, input_code.RIGHT])
                or range_input < self.config.min_launch_range or range_input > self.config.max_launch_range):
            raise input_code.InvalidCommandException()
        self.message = (input_code.get_direction_message(command_input), range_input)  # update weapon message as firing direction and range
        return self


# weapons
assulter_rifle = StraightWeapon(StraightWeaponConfig("assulter rifle", dmg.Damage(80, 3), 0.75, 0.03, 8, 6, 4, 40))
submachine_gun = StraightWeapon(StraightWeaponConfig("submachine gun", dmg.Damage(70, 2), 0.85, 0.03, 6, 5, 3, 65))
pistol = StraightWeapon(StraightWeaponConfig("pistol", dmg.Damage(60, 2), 0.95, 0.02, 5, 4, 2, 90))
sniper_rifle = StraightWeapon(StraightWeaponConfig("sniper_rifle", dmg.Damage(100, 4), 0.2, -0.03, 12, 6, 5, 10))
shotgun = StraightWeapon(StraightWeaponConfig("shotgun", dmg.Damage(100, 1), 1, 0.15, 4, 7, 4, 30))

# projectile weapons
impact_grenade = ProjectileWeapon(ProjectileWeaponConfig("impact grenade", dmg.Damage(40, 1), 4, 6, 3, 10, 4, 2, 60))
frag_grenade = ProjectileWeapon(ProjectileWeaponConfig("frag grenade", dmg.Damage(60, 2), 3, 6, 2, 20, 5, 3, 30))
breaching_grenade = ProjectileWeapon(ProjectileWeaponConfig("breaching grenade", dmg.Damage(5, 5), 3, 5, 2, 0, 5, 2, 80))
