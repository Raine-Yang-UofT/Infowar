"""
Handle weapon detection
"""
from battlefield import Battlefield
from interface import IDamageable, Damage, StraightDamage
import Framework.message as message


class RobotWeapons:

    def __init__(self, battlefield: Battlefield):
        self.battlefield = battlefield

    def shoot_straight_weapon(self, x: int, y: int, direction: int, damage: StraightDamage):
        """
        Fire the weapon from (x, y) at a given direction. The weapon deals
        certain damage to the target hit

        :param x: the x-coordinate of starting point
        :param y: the y-coordinate of the starting point
        :param direction: the direction of shooting
        :param damage: the damage of the weapon
        :return: None
        """
        # set shooting direction
        dx, dy = 0, 0
        if direction == message.UP:
            dy = -1
        elif direction == message.DOWN:
            dy = 1
        elif direction == message.LEFT:
            dx = -1
        elif direction == message.RIGHT:
            dx = 1

        distance = 0
        # find the first target hit
        while not self.battlefield.is_occupied(x, y):
            x += dx
            y += dy
            damage.accuracy -= damage.accuracy_decay    # reduce weapon accuracy through distance
            distance += 1
            if distance >= damage.range:
                break

        # deals damage to the target
        if isinstance(self.battlefield.get_grid(x, y).get_occupant(), IDamageable):
            self.battlefield.get_grid(x, y).get_occupant().get_damage(damage)
