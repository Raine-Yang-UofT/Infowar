"""
Handle weapon detection
"""
from battlefield import Battlefield
from Framework.interface import IDamageable
from Items import weapons
import Framework.message as message
import random
from dataclasses import replace


class RobotWeapons:

    def __init__(self, battlefield: Battlefield):
        self.battlefield = battlefield

    def shoot_straight_weapon(self, x: int, y: int, weapon: weapons.StraightWeapon) -> str:
        """
        Fire the weapon from (x, y) at a given direction. The weapon deals
        certain damage to the target hit

        :param x: the x-coordinate of starting point
        :param y: the y-coordinate of the starting point
        :param weapon: the weapon used
        :return: the target hit by the weapon
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
            return 'weapon missed!'

        # deals damage to the target
        occupant = self.battlefield.get_grid(px, py).get_occupant()
        if isinstance(occupant, IDamageable):
            print(self.battlefield.get_grid(px, py).get_occupant())
            # check whether the target is hit
            if random.random() <= accuracy:
                occupant.get_damage(damage)
                return 'weapon hit ' + occupant.get_name() + '!'

        return 'weapon missed!'

    def shoot_projectile_weapon(self, x: int, y: int, weapon: weapons.ProjectileWeapon) -> list[str]:
        """
        Fire a projectile weapon from (x, y) at a given direction and range. The weapon deals
        certain damage to the target hit

        :param x: the x-coordinate of starting point
        :param y: the y-coordinate of the starting point
        :param weapon: the weapon used
        :return: the targets hit by the weapon
        """
        targets = []

        # generate sound and heat at starting position
        self.battlefield.generate_heat(x, y, weapon.heat_emission)

        # set target location
        px, py = x, y
        if weapon.message[0] == message.UP:
            py -= weapon.message[1]
        elif weapon.message[0] == message.DOWN:
            py += weapon.message[1]
        elif weapon.message[0] == message.LEFT:
            px -= weapon.message[1]
        elif weapon.message[0] == message.RIGHT:
            px += weapon.message[1]

        # examine the grids in the range
        for i in range(0, len(self.battlefield.field[0])):
            for j in range(0, len(self.battlefield.field)):
                if (i - px) ** 2 + (j - py) ** 2 <= weapon.impact_radius ** 2:
                    # prevent index out of bound
                    if i < 0 or i >= len(self.battlefield.field[0]) or j < 0 or j >= len(self.battlefield.field):
                        continue
                    # deals damage to the target
                    occupant = self.battlefield.get_grid(i, j).get_occupant()
                    if isinstance(occupant, IDamageable):
                        # calculate damage decay
                        net_damage = weapon.damage.damage - weapon.impact_damage_decay * int(((i - px) ** 2 + (j - py) ** 2) ** 0.5)
                        occupant.get_damage(replace(weapon.damage, damage=net_damage))
                        targets.append("weapon hit " + occupant.get_name() + '!')

        return targets
