"""
A Module containing all interface definitions
"""
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

    def get_name(self) -> str:
        """
        Return the name of the object

        :return: the name of the object
        """
        # Override in children class
        return 'the get_name method is not implemented in child class'


class ISensor:
    """
    ISensor: an object can receive player input and sense signals

    child classes should implement detect_signal() and select_sensor_parameter() methods
    """
    def detect_signal(self, sensors, robot) -> None:
        """
        Detect signal at a square region with a given radius around player

        :param sensors: the RobotSensor observer class
        :param robot: the robot that detects the signal
        :return: None
        """
        # Override in children class

    def select_sensor_parameter(self):
        """
        Add additional parameters to sensor

        :return: a copy of sensor object with updated parameters
        """
        # Override in children class


class IWeapon:
    """
    IWeapon: an object can be used as a weapon

    child classes should implement fire_weapon() and select_weapon_parameter() methods
    """
    def fire_weapon(self, weapons, robot) -> None:
        """
        Fire weapon from robot

        :param weapons: the RobotWeapons observer class
        :param robot: the robot that fires the weapon
        :return: None
        """
        # Override in children class

    def select_weapon_parameter(self):
        """
        Add additional parameters to weapon

        :return: a copy of weapon object with updated parameters
        """
        # Override in children class

