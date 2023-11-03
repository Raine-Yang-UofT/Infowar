"""
Handle sensor detection
"""
from battlefield import Battlefield


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

    def display_signal_vision(self, x: int, y: int, signal_type: str, radius: int) -> list[list[int]]:
        """
        Show the sound/heat signal centered at (x, y) at a given radius

        :param x: the x-coordinate of detection point
        :param y: the y-coordinate of detection point
        :param signal_type: the type of signal (sound/heat)
        :param radius: the radius of signal (square region)
        :return: the signal to display
        """
        result = []
        for i in range(0, len(self.battlefield.field)):
            row = []
            for j in range(0, len(self.battlefield.field[0])):
                if y - radius <= i <= y + radius and x - radius <= j <= x + radius:
                    if signal_type == 'sound':
                        row.append(self.battlefield.get_grid(j, i).get_sound())
                    elif signal_type == 'heat':
                        row.append(self.battlefield.get_grid(j, i).get_heat())
                    else:
                        print('Unrecognized signal type')
            result.append(row)

        return result
