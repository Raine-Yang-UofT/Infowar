"""
Sensor items
"""
from dataclasses import dataclass
from dataclasses import replace
from Framework import interface, message
from Framework import input_code


@dataclass(frozen=True)
class SoundSensor(interface.ISensor):
    """
    Detect sound signal at a square region with a given radius around player

        - name: the name of sensor
        - radius: the detection radius
        - message: the message associated with the sensor
    """
    name: str
    radius: int
    message: int

    def detect_signal(self, sensors, robot) -> None:
        """
        Detect sound signal at a square region with a given radius around player

        :param sensors: the RobotSensor observer class
        :param robot: the robot that detects the signal
        :return: None
        """
        sound_signal = sensors.display_signal_vision(robot.get_pos()[0], robot.get_pos()[1], self)
        robot.receive_info(
            "Sound signal detected at (" + str(robot.get_pos()[0]) + ", " + str(robot.get_pos()[1]) + ")")
        robot.receive_info("Sound signal: ")
        robot.receive_info(sound_signal)

    def select_sensor_parameter(self):
        """
        No additional parameters for sound sensor

        :return: the parameter of the sensor
        """
        return self


@dataclass(frozen=True)
class HeatSensor(interface.ISensor):
    """
    Detect heat signal at a square region with a given radius around player

        - name: the name of sensor
        - radius: the detection radius
        - message: the message associated with the sensor
    """
    name: str
    radius: int
    message: int

    def detect_signal(self, sensors, robot) -> None:
        """
        Detect heat signal at a square region with a given radius around player

        :param sensors: the RobotSensor observer class
        :param robot: the robot that detects the signal
        :return: None
        """
        heat_signal = sensors.display_signal_vision(robot.get_pos()[0], robot.get_pos()[1], self)
        robot.receive_info(
            "Heat signal detected at (" + str(robot.get_pos()[0]) + ", " + str(robot.get_pos()[1]) + ")")
        robot.receive_info("Heat signal: ")
        robot.receive_info(heat_signal)

    def select_sensor_parameter(self):
        """
        No additional parameters for heat sensor

        :return: the parameter of the sensor
        """
        return self


@dataclass(frozen=True)
class Lidar(interface.ISensor):
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

    def detect_signal(self, sensors, robot) -> None:
        """
        Detect a square range around player and update the map

        :param sensors: the RobotSensor observer class
        :param robot: the robot that detects the signal
        :return: None
        """
        lidar_view = sensors.display_lidar_vision(robot.get_pos()[0], robot.get_pos()[1], self)
        robot.receive_info(
            "Complete lidar scanning at (" + str(robot.get_pos()[0]) + ", " + str(robot.get_pos()[1]) + ")")
        robot.receive_info(lidar_view)
        robot.update_map(lidar_view)

    def select_sensor_parameter(self):
        """
        No additional parameters for lidar

        :return: the parameter of the sensor
        """
        return self


@dataclass(frozen=True)
class Drone(interface.ISensor):
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
    """
    name: str
    radius: int
    sound_emission: int
    heat_emission: int
    message: int
    commands: str
    longest_range: int

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
        if not (all([c in ['w', 'a', 's', 'd'] for c in command]) and len(command) <= self.longest_range):
            print("Invalid drone path, make sure the path only contains (w, a, s, d) and is shorter than " + str(
                self.longest_range) + " steps")
            raise input_code.InvalidCommandException()
        # update drone path
        print("drone path updated")
        return replace(self, commands=command)


@dataclass(frozen=True)
class ScoutCar(interface.ISensor):
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
        - max_barricade_remove: the maximum number of barricades the scout car can remove
    """
    name: str
    radius: int
    sound_emission: int
    heat_emission: int
    message: int
    direction: str
    max_barricade_remove: int

    def detect_signal(self, sensors, robot) -> None:
        """
        Detect a square range around player and update the map

        :param sensors: the RobotSensor observer class
        :param robot: the robot that detects the signal
        :return: None
        """
        scout_car_view = sensors.display_scout_car_vision(robot.get_pos()[0], robot.get_pos()[1], self)
        robot.receive_info(
            "Scout car scanning at (" + str(scout_car_view[1][0]) + ", " + str(scout_car_view[1][1]) + ")")
        robot.receive_info(scout_car_view[0])
        robot.update_map(scout_car_view[0])

    def select_sensor_parameter(self):
        """
        Add additional parameters to scout car

        :return: the scout car with updated parameters
        """
        direction = input("Enter (w, a, s, d) to map the direction of scout car: ")
        if direction not in ['w', 'a', 's', 'd']:
            print("Invalid scout car direction, make sure the direction is one of (w, a, s, d)")
            raise input_code.InvalidCommandException()
        # update scout car direction
        print("scout car direction updated")
        return replace(self, direction=direction)


# sensor objects
heat_sensor = HeatSensor(name="heat sensor", radius=5, message=message.SENSE_HEAT)
sound_sensor = SoundSensor(name="sound sensor", radius=5, message=message.SENSE_SOUND)
lidar = Lidar(name="lidar", radius=3, sound_emission=2, heat_emission=5, message=message.SENSE_LIDAR)
drone = Drone(name='drone', radius=2, sound_emission=6, heat_emission=2, message=message.SENSE_DRONE, commands='', longest_range=10)
scout_car = ScoutCar(name='scout car', radius=2, sound_emission=4, heat_emission=2, message=message.SENSE_SCOUT_CAR, direction='', max_barricade_remove=3)
