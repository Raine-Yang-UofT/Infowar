"""
Handle sensor detection
"""
from battlefield import Battlefield
import Items.sensors as sensors
import Framework.message as message


class RobotSensor:

    def __init__(self, field: Battlefield):
        self.battlefield = field

    def display_player_vision(self, x: int, y: int) -> list[list[str]]:
        """
        Display the 3 * 3 region of the grid in player's vision, the rest of
        the grids are displayed as empty space

        :param x: the x-ccordinate of player
        :param y: the y-coordinate of player
        :return: a string representation of player's vision at the location
        """
        result = []
        for i in range(0, len(self.battlefield.field)):
            row = []
            for j in range(0, len(self.battlefield.field[0])):
                if y - 1 <= i <= y + 1 and x - 1 <= j <= x + 1:
                    row.append(self.battlefield.get_grid(j, i).display())
                else:
                    row.append(' ')

            result.append(row)

        return result

    def display_signal_vision(self, x: int, y: int, sensor: sensors.SignalSensor) -> list[list[int]]:
        """
        Show the sound/heat signal centered at (x, y) at a given radius

        :param x: the x-coordinate of detection point
        :param y: the y-coordinate of detection point
        :param sensor: the sensor used to detect the signal
        :return: the signal to display
        """
        result = []
        for i in range(0, len(self.battlefield.field)):
            row = []
            for j in range(0, len(self.battlefield.field[0])):
                if y - sensor.radius <= i <= y + sensor.radius and x - sensor.radius <= j <= x + sensor.radius:
                    if sensor.message == message.SENSE_SOUND:
                        row.append(self.battlefield.get_grid(j, i).get_sound())
                    elif sensor.message == message.SENSE_HEAT:
                        row.append(self.battlefield.get_grid(j, i).get_heat())
                    else:
                        print('Unrecognized signal type')
            result.append(row)

        return result

    def display_lidar_vision(self, x: int, y: int, lidar: sensors.Lidar) -> list[list[str]]:
        """
        Show the lidar detection centered at (x, y) at a given radius
        Emit sound and heat signal around the detection point

        :param x: the x-coordinate of detection point
        :param y: the y-coordinate of detection point
        :param lidar: the lidar used to detect the signal
        :return: the signal to display
        """
        # create grid
        result = []
        for i in range(0, len(self.battlefield.field)):
            row = []
            for j in range(0, len(self.battlefield.field[0])):
                if y - lidar.radius <= i <= y + lidar.radius and x - lidar.radius <= j <= x + lidar.radius:
                    row.append(self.battlefield.get_grid(j, i).display())
                else:
                    row.append(' ')
            result.append(row)

        # emit sound and heat
        self.battlefield.generate_sound(x, y, lidar.sound_emission)
        self.battlefield.generate_heat(x, y, lidar.heat_emission)

        return result
