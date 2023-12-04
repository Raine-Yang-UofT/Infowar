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
        self.battlefield.generate_sound(x, y, weapon.config.sound_emission)
        self.battlefield.generate_heat(x, y, weapon.config.heat_emission)

        # set shooting direction
        dx, dy = 0, 0
        px, py = x, y
        if weapon.direction == message.UP:
            dy = -1
        elif weapon.direction == message.DOWN:
            dy = 1
        elif weapon.direction == message.LEFT:
            dx = -1
        elif weapon.direction == message.RIGHT:
            dx = 1

        distance = 1
        # initial displacement
        px += dx
        py += dy
        damage = weapon.config.damage
        accuracy = weapon.config.accuracy
        # find the first target hit
        while not self.battlefield.is_occupied(px, py):
            px += dx
            py += dy
            accuracy -= weapon.config.accuracy_decay    # reduce weapon accuracy through distance
            distance += 1
            if distance >= weapon.config.range:
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
        self.battlefield.generate_heat(x, y, weapon.config.heat_emission)
        self.battlefield.generate_heat(x, y, weapon.config.sound_emission)

        # set target location
        px, py = x, y
        if weapon.direction == message.UP:
            py -= weapon.range
        elif weapon.direction == message.DOWN:
            py += weapon.range
        elif weapon.direction == message.LEFT:
            px -= weapon.range
        elif weapon.direction == message.RIGHT:
            px += weapon.range

        # examine the grids in the range
        for i in range(max(0, px - weapon.config.impact_radius), min(len(self.battlefield.field[0]), px + weapon.config.impact_radius + 1)):
            for j in range(max(0, py - weapon.config.impact_radius), min(len(self.battlefield.field), py + weapon.config.impact_radius + 1)):
                if (i - px) ** 2 + (j - py) ** 2 <= weapon.config.impact_radius ** 2:
                    # deals damage to the target
                    occupant = self.battlefield.get_grid(i, j).get_occupant()
                    if isinstance(occupant, IDamageable):
                        # calculate damage decay
                        net_damage = weapon.config.damage.damage - weapon.config.impact_damage_decay * int(((i - px) ** 2 + (j - py) ** 2) ** 0.5)
                        occupant.get_damage(replace(weapon.config.damage, damage=net_damage))
                        targets.append("weapon hit " + occupant.get_name() + '!')

        return targets
