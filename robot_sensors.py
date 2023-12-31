"""
Handle sensor detection
"""
import Items.sensors as sensors
from Framework import message


class RobotSensor:

    def __init__(self, game):
        self.game = game
        self.battlefield = game.battlefield

    def display_player_vision(self, x: int, y: int) -> list[list[str]]:
        """
        Display the 3 * 3 region of the grid in player's vision, the rest of
        the grids are displayed as empty space

        :param x: the x-ccordinate of player
        :param y: the y-coordinate of player
        :return: a string representation of player's vision at the location
        """
        return self.display_grid_helper(x, y, 1)

    def display_grid_helper(self, x: int, y: int, radius: int) -> list[list[str]]:
        """
        Helper method, display a square region centered at (x, y) with a given radius
        Part of map outside the region is displayed as empty space

        :param x: the x-coordinate of the center
        :param y: the y-coordinate of the center
        :param radius: the radius of the square region
        :return: a string representation of the square region
        """
        result = []
        for i in range(0, len(self.battlefield.field)):
            row = []
            for j in range(0, len(self.battlefield.field[0])):
                if y - radius <= i <= y + radius and x - radius <= j <= x + radius:
                    row.append(self.battlefield.get_grid(j, i).display())
                else:
                    row.append('*')
            result.append(row)

        return result

    def display_signal_vision(self, x: int, y: int, sensor) -> list[list]:
        """
        Show the sound/heat signal centered at (x, y) at a given radius

        :param x: the x-coordinate of detection point
        :param y: the y-coordinate of detection point
        :param sensor: the sensor used to detect the signal
        :return: the signal to display
        """
        result = [['*' for _ in range(0, len(self.battlefield.field[0]))] for _ in range(0, len(self.battlefield.field))]
        for i in range(0, len(self.battlefield.field)):
            for j in range(0, len(self.battlefield.field[0])):
                if y - sensor.config.radius <= i <= y + sensor.config.radius and x - sensor.config.radius <= j <= x + sensor.config.radius:
                    # TODO: refactor this part if more types of signals are added
                    if isinstance(sensor, sensors.SoundSensor):
                        result[i][j] = self.battlefield.get_grid(j, i).get_sound()
                    elif isinstance(sensor, sensors.HeatSensor):
                        result[i][j] = self.battlefield.get_grid(j, i).get_heat()
                    else:
                        print('Unrecognized signal type')

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
        # emit sound and heat
        self.battlefield.generate_sound(x, y, lidar.config.sound_emission)
        self.battlefield.generate_heat(x, y, lidar.config.heat_emission)

        return self.display_grid_helper(x, y, lidar.config.radius)

    def display_drone_vision(self, x: int, y: int, drone: sensors.Drone) -> [list[list[str]], tuple[int, int]]:
        """
        Show the drone scanning started from (x, y)
        Emit sound and heat signal around (x, y)

        :param x: the x-coordinate of starting point
        :param y: the y-coordinate of starting point
        :param drone: the drone used to scan
        :return: the signal to display
        """
        # move to the destinated location
        drone_x, drone_y = x, y
        for direction in drone.commands:
            if direction == 'w' and drone_y > 0:
                drone_y -= 1
            elif direction == 'a' and drone_x > 0:
                drone_x -= 1
            elif direction == 's' and drone_y < len(self.battlefield.field) - 1:
                drone_y += 1
            elif direction == 'd' and drone_x < len(self.battlefield.field[0]) - 1:
                drone_x += 1

        self.battlefield.generate_sound(x, y, drone.config.sound_emission)
        self.battlefield.generate_heat(x, y, drone.config.heat_emission)

        return self.display_grid_helper(drone_x, drone_y, drone.config.radius), (drone_x, drone_y)

    def display_scout_car_vision(self, x: int, y: int, scout_car: sensors.ScoutCar) -> [list[list[str]], tuple[int, int]]:
        """
        Show the scout car scanning started from (x, y)
        Emit sound and heat signal around (x, y)

        :param x: the x-coordinate of starting point
        :param y: the y-coordinate of starting point
        :param scout_car: the scout car used to scan
        :return: the signal to display
        """
        # move to the destinated location
        car_x, car_y = x, y
        # determine movement direction
        vx, vy = 0, 0
        if scout_car.direction == message.UP and car_y > 0:
            vy = -1
        elif scout_car.direction == message.LEFT and car_x > 0:
            vx = -1
        elif scout_car.direction == message.DOWN and car_y < len(self.battlefield.field) - 1:
            vy = 1
        elif scout_car.direction == message.RIGHT and car_x < len(self.battlefield.field[0]) - 1:
            vx = 1

        max_barricade_remove = scout_car.config.max_barricade_remove
        # move along the direction while breaking the barricades along the way
        while self.battlefield.get_grid(car_x + vx, car_y + vy) is not None and not self.battlefield.is_blocked(car_x + vx, car_y + vy):
            # update car location
            car_x += vx
            car_y += vy
            # remove barricades
            if self.battlefield.get_grid(car_x, car_y) is not None and self.battlefield.get_grid(car_x, car_y).display() == 'x':
                if max_barricade_remove > 0:
                    self.battlefield.get_grid(car_x, car_y).remove_occupant()
                    max_barricade_remove -= 1
                else:
                    break

        self.battlefield.generate_sound(x, y, scout_car.config.sound_emission)
        self.battlefield.generate_heat(x, y, scout_car.config.heat_emission)

        return self.display_grid_helper(car_x, car_y, scout_car.config.radius), (car_x, car_y)
