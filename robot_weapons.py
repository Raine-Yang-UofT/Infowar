"""
Handle weapon detection
"""
from battlefield import Battlefield
from interface import IDamageable
from Items import weapons
import Framework.message as message
import random


class RobotWeapons:

    def __init__(self, battlefield: Battlefield):
        self.battlefield = battlefield

    def shoot_straight_weapon(self, x: int, y: int, weapon: weapons.StraightWeapon) -> None:
        """
        Fire the weapon from (x, y) at a given direction. The weapon deals
        certain damage to the target hit

        :param x: the x-coordinate of starting point
        :param y: the y-coordinate of the starting point
        :param weapon: the weapon used
        :return: None
        """
        # generate sound and heat at starting position
        self.battlefield.generate_sound(x, y, weapon.sound_emission)
        self.battlefield.generate_heat(x, y, weapon.heat_emission)

        # set shooting direction
        dx, dy = 0, 0
        px, py = x, y
        if weapon.message == message.UP:
            dy = -1
        elif weapon.message == message.DOWN:
            dy = 1
        elif weapon.message == message.LEFT:
            dx = -1
        elif weapon.message == message.RIGHT:
            dx = 1

        distance = 1
        # initial displacement
        px += dx
        py += dy
        damage = weapon.damage
        accuracy = weapon.accuracy
        # find the first target hit
        while not self.battlefield.is_occupied(px, py):
            px += dx
            py += dy
            accuracy -= weapon.accuracy_decay    # reduce weapon accuracy through distance
            distance += 1
            if distance >= weapon.range:
                break

        # prevent out-of-bound index
        px = max(0, min(px, len(self.battlefield.field[0]) - 1))
        py = max(0, min(py, len(self.battlefield.field) - 1))

        # prevent hitting player itself
        if px == x and py == y:
            return

        # deals damage to the target
        if isinstance(self.battlefield.get_grid(px, py).get_occupant(), IDamageable):
            # check whether the target is hit
            if random.random() <= accuracy:
                self.battlefield.get_grid(px, py).get_occupant().get_damage(damage)
