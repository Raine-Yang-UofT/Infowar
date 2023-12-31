"""
The configurations for robots, sensors, weapons, and gadgets
"""
from dataclasses import dataclass
import Items.sensors as sensors
import Items.weapons as weapons
import Items.gadgets as gadgets


@dataclass
class Armor:
    """
    configurations for robot armor

        - max_armor: the maximum armor value
        - armor_reduction_rate: the probably that armor decreases after each damage
        - armor_protection: the percentage of damage absorbed by armor
    """
    max_armor: int
    armor_reduction_rate: float
    armor_protection: float


@dataclass
class RobotConfig:
    """
    configurations for robot

        - HP: the robot's HP
        - armor: the robot's armor
        - move_sound: the sound generated when robot moves
        - move_heat: the heat generated when robot moves
        - sensors: the sensors equipped
        - weapons: the weapons equipped
        - gadgets: the gadgets equipped and their total uses
    """
    HP: int
    armor: Armor
    move_sound: int
    move_heat: int
    move_speed: int
    sensors: list
    weapons: list
    gadgets: list


# armors
light_composite_armor = Armor(2, 0.4, 0.6)
standard_composite_armor = Armor(3, 0.4, 0.6)
improved_composite_armor = Armor(4, 0.4, 0.6)
heavy_composite_armor = Armor(5, 0.4, 0.6)

light_porcelain_armor = Armor(2, 0.6, 0.8)
standard_porcelain_armor = Armor(3, 0.6, 0.8)
improved_porcelain_armor = Armor(4, 0.6, 0.8)
heavy_porcelain_armor = Armor(5, 0.6, 0.8)

light_steel_armor = Armor(2, 0.2, 0.4)
standard_steel_armor = Armor(3, 0.2, 0.4)
improved_steel_armor = Armor(4, 0.2, 0.4)
heavy_steel_armor = Armor(5, 0.2, 0.4)


# a default configuration for testing
default_config = RobotConfig(
    HP=100,
    armor=standard_composite_armor,
    move_sound=5,
    move_heat=3,
    move_speed=50,
    sensors=[sensors.heat_sensor, sensors.sound_sensor, sensors.lidar, sensors.drone, sensors.scout_car],
    weapons=[weapons.assulter_rifle, weapons.submachine_gun, weapons.pistol, weapons.sniper_rifle, weapons.shotgun, weapons.impact_grenade, weapons.frag_grenade, weapons.breaching_grenade],
    gadgets=[gadgets.deployable_barricade, gadgets.EMP_bomb, gadgets.flash_bomb, gadgets.repair_kit]
)
