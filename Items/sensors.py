"""
Sensor items
"""
from dataclasses import dataclass
from Framework import interface
from Framework import input_code
from Items import prompt_template as prompt


@dataclass(frozen=True)
class SignalSensorConfig:
    """
    Detect signal at a square region with a given radius around player

        - name: the name of sensor
        - radius: the detection radius
    """
    name: str
    radius: int


class SoundSensor(interface.ISensor):
    """
    Detect sound signal at a square region with a given radius around player
    """
    def __init__(self, config: SignalSensorConfig):
        self.config = config

    def detect_signal(self, sensors, robot) -> None:
        """
        Detect sound signal at a square region with a given radius around player

        :param sensors: the RobotSensor observer class
        :param robot: the robot that detects the signal
        :return: None
        """
        sound_signal = sensors.display_signal_vision(robot.get_pos()[0], robot.get_pos()[1], self)
        robot.receive_info("Sound signal detected at (" + str(robot.get_pos()[0]) + ", " + str(robot.get_pos()[1]) + ")")
        robot.receive_info("Sound signal: ")
        robot.receive_info(sound_signal)

    def select_sensor_parameter(self):
        """
        No additional parameters for sound sensor

        :return: the parameter of the sensor
        """
        return self


class HeatSensor(interface.ISensor):
    """
    Detect heat signal at a square region with a given radius around player
    """
    def __init__(self, config: SignalSensorConfig):
        self.config = config

    def detect_signal(self, sensors, robot) -> None:
        """
        Detect heat signal at a square region with a given radius around player

        :param sensors: the RobotSensor observer class
        :param robot: the robot that detects the signal
        :return: None
        """
        heat_signal = sensors.display_signal_vision(robot.get_pos()[0], robot.get_pos()[1], self)
        robot.receive_info("Heat signal detected at (" + str(robot.get_pos()[0]) + ", " + str(robot.get_pos()[1]) + ")")
        robot.receive_info("Heat signal: ")
        robot.receive_info(heat_signal)

    def select_sensor_parameter(self):
        """
        No additional parameters for heat sensor

        :return: the parameter of the sensor
        """
        return self


@dataclass(frozen=True)
class LidarConfig:
    """
    Detect a square range around player and update the map

        - name: the name of sensor
        - radius: the detection radius
        - sound_emission: the sound emission of the sensor
        - heat_emission: the heat emission of the sensor
    """
    name: str
    radius: int
    sound_emission: int
    heat_emission: int


class Lidar(interface.ISensor):
    """
    Detect a square range around player and update the map
    """
    def __init__(self, config: LidarConfig):
        self.config = config

    def detect_signal(self, sensors, robot) -> None:
        """
        Detect a square range around player and update the map

        :param sensors: the RobotSensor observer class
        :param robot: the robot that detects the signal
        :return: None
        """
        lidar_view = sensors.display_lidar_vision(robot.get_pos()[0], robot.get_pos()[1], self)
        robot.receive_info("Complete lidar scanning at (" + str(robot.get_pos()[0]) + ", " + str(robot.get_pos()[1]) + ")")
        robot.receive_info(lidar_view)
        robot.update_map(lidar_view)

    def select_sensor_parameter(self):
        """
        No additional parameters for lidar

        :return: the parameter of the sensor
        """
        return self


@dataclass(frozen=True)
class DroneConfig:
    """
    Move to a certain location based on player's command
    and detect a square region around the location

        - name: the name of sensor
        - radius: the detection radius
        - sound_emission: the sound emission of the sensor
        - heat_emission: the heat emission of the sensor
        - longest_range: the longest path the drone can move (maximum command length)
    """
    name: str
    radius: int
    sound_emission: int
    heat_emission: int
    longest_range: int


class Drone(interface.ISensor):
    """
    Move the drone to a certain location based on player's command
    """
    def __init__(self, config: DroneConfig):
        self.config = config
        self.commands = ''

    def detect_signal(self, sensors, robot) -> None:
        """
        Detect a square range around player and update the map

        :param sensors: the RobotSensor observer class
        :param robot: the robot that detects the signal
        :return: None
        """
        drone_view = sensors.display_drone_vision(robot.get_pos()[0], robot.get_pos()[1], self)
        robot.receive_info("Drone scanning at (" + str(drone_view[1][0]) + ", " + str(drone_view[1][1]) + ")")
        robot.receive_info(drone_view[0])
        robot.update_map(drone_view[0])

    def select_sensor_parameter(self):
        """
        Add additional parameters to drone

        :return: the drone with updated parameters
        """
        command = input("Enter (w, a, s, d) to map the path of drone: ")
        if not (all([c in ['w', 'a', 's', 'd'] for c in command]) and len(command) <= self.config.longest_range):
            print("Invalid drone path, make sure the path only contains (w, a, s, d) and is shorter than " + str(self.config.longest_range) + " steps")
            raise input_code.InvalidCommandException()
        # update drone path
        print("drone path updated")
        self.commands = command
        return self


@dataclass(frozen=True)
class ScoutCarConfig:
    """
    Move to a certain location based on player's command
    and detect a square region around the location
    can be blocked by barricades

        - name: the name of sensor
        - radius: the detection radius
        - sound_emission: the sound emission of the sensor
        - heat_emission: the heat emission of the sensor
        - max_barricade_remove: the maximum number of barricades the scout car can remove
    """
    name: str
    radius: int
    sound_emission: int
    heat_emission: int
    max_barricade_remove: int


class ScoutCar(interface.ISensor):
    """
    Move the scout car to a certain location based on player's command
    """
    def __init__(self, config: ScoutCarConfig):
        self.config = config
        self.direction = -1

    def detect_signal(self, sensors, robot) -> None:
        """
        Detect a square range around player and update the map

        :param sensors: the RobotSensor observer class
        :param robot: the robot that detects the signal
        :return: None
        """
        scout_car_view = sensors.display_scout_car_vision(robot.get_pos()[0], robot.get_pos()[1], self)
        robot.receive_info("Scout car scanning at (" + str(scout_car_view[1][0]) + ", " + str(scout_car_view[1][1]) + ")")
        robot.receive_info(scout_car_view[0])
        robot.update_map(scout_car_view[0])

    def select_sensor_parameter(self):
        """
        Add additional parameters to scout car

        :return: the scout car with updated parameters
        """
        return prompt.select_direction(self, "Select the direction to move scout car:")


# sensor objects
heat_sensor = HeatSensor(
    SignalSensorConfig(
        name="heat sensor",
        radius=5
    )
)

sound_sensor = SoundSensor(
    SignalSensorConfig(
        name="sound sensor",
        radius=5
    )
)

lidar = Lidar(
    LidarConfig(
        name="lidar",
        radius=3,
        sound_emission=2,
        heat_emission=2
    )
)

drone = Drone(
    DroneConfig(
        name='drone',
        radius=2,
        sound_emission=6,
        heat_emission=2,
        longest_range=10
    )
)

scout_car = ScoutCar(
    ScoutCarConfig(
        name='scout car',
        radius=2,
        sound_emission=4,
        heat_emission=2,
        max_barricade_remove=2
    )
)
