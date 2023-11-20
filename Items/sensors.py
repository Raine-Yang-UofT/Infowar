"""
Sensor items
"""
from dataclasses import dataclass
from Framework import message


@dataclass(frozen=True)
class SignalSensor:
    """
    Detect signal at a square region with a given radius around player

        - name: the name of sensor
        - radius: the detection radius
        - message: the message associated with the sensor
    """
    name: str
    radius: int
    message: int


@dataclass(frozen=True)
class Lidar:
    """
    Detect a square range around player and update the map

        - name: the name of sensor
        - radius: the detection radius
        - sound_emission: the sound emission of the sensor
        - heat_emission: the heat emission of the sensor
        - message: the message associated with the sensor
    """
    name: str
    radius: int
    sound_emission: int
    heat_emission: int
    message: int


@dataclass(frozen=True)
class Drone:
    """
    Move to a certain location based on player's command
    and detect a square region around the location

        - name: the name of sensor
        - radius: the detection radius
        - sound_emission: the sound emission of the sensor
        - heat_emission: the heat emission of the sensor
        - message: the message associated with the sensor
        - commands: the commands inputed by player
        - longest_range: the longest path the drone can move (maximum command length)
        - location: the final location of the drone
    """
    name: str
    radius: int
    sound_emission: int
    heat_emission: int
    message: int
    commands: str
    longest_range: int
    location: tuple[int, int]


@dataclass(frozen=True)
class ScoutCar:
    """
    Move to a certain location based on player's command
    and detect a square region around the location
    can be blocked by barricades

        - name: the name of sensor
        - radius: the detection radius
        - sound_emission: the sound emission of the sensor
        - heat_emission: the heat emission of the sensor
        - message: the message associated with the sensor
        - direction: the direction of cat movement
        - location: the final location of the drone
        - max_barricade_remove: the maximum number of barricades the scout car can remove
    """
    name: str
    radius: int
    sound_emission: int
    heat_emission: int
    message: int
    direction: str
    location: tuple[int, int]
    max_barricade_remove: int


# sensor objects
heat_sensor = SignalSensor(name="heat sensor", radius=5, message=message.SENSE_HEAT)
sound_sensor = SignalSensor(name="sound sensor", radius=5, message=message.SENSE_SOUND)
lidar = Lidar(name="lidar", radius=3, sound_emission=2, heat_emission=5, message=message.SENSE_LIDAR)
drone = Drone(name='drone', radius=2, sound_emission=6, heat_emission=2, message=message.SENSE_DRONE, commands='', longest_range=10, location=(0, 0))
scout_car = ScoutCar(name='scout car', radius=2, sound_emission=4, heat_emission=2, message=message.SENSE_SCOUT_CAR, direction='', location=(0, 0), max_barricade_remove=3)
