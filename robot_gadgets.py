"""
Handle gadget use
"""
from battlefield import Battlefield
import Framework.message as message
import barricade
from Items import gadgets


class RobotGadgets:

    def __init__(self, field: Battlefield):
        self.battlefield = field

    def deploy_barricade(self, x: int, y: int, gadget: gadgets.DeployableBarricade) -> str:
        """
        Deploy a hard barricade at a certain direction from (x, y)

        :param x: the x-coordinate of the deployment point
        :param y: the y-coordinate of the deployment point
        :param gadget: the hard barricade to deploy
        :return: result on deployment
        """
        px, py = x, y
        if gadget.direction == message.UP:
            py -= 1
        elif gadget.direction == message.DOWN:
            py += 1
        elif gadget.direction == message.LEFT:
            px -= 1
        elif gadget.direction == message.RIGHT:
            px += 1

        if self.battlefield.is_blocked(px, py):
            return 'Deployment failed: the location has been blocked'

        grid = self.battlefield.get_grid(px, py)
        grid.change_occupant(barricade.HardBarricade(gadget.config.HP, gadget.config.armor, grid))

        return f'Deploy barricade at ({px}, {py})'

    def throw_EMP_bomb(self, x: int, y: int, gadget: gadgets.EMPBomb) -> str:
        """
        Throw an EMP bomb at a certain direction and range from (x, y)

        :param x: the x-coordinate of the starting point
        :param y: the y-coordinate of the starting point
        :param gadget: the EMP bomb to throw
        :return: result on throwing
        """
        px, py = x, y
        if gadget.direction == message.UP:
            py -= 1
        elif gadget.direction == message.DOWN:
            py += 1
        elif gadget.direction == message.LEFT:
            px -= 1
        elif gadget.direction == message.RIGHT:
            px += 1

        # generate sound and heat at starting position
        self.battlefield.generate_sound(x, y, gadget.config.sound_emission)
        self.battlefield.generate_heat(x, y, gadget.config.heat_emission)

        # find the targets in range
        targets = []
        for i in range(max(0, px - gadget.config.impact_radius), min(len(self.battlefield.field[0]), px + gadget.config.impact_radius + 1)):
            for j in range(max(0, py - gadget.config.impact_radius), min(len(self.battlefield.field), py + gadget.config.impact_radius + 1)):
                if (i - px) ** 2 + (j - py) ** 2 <= gadget.config.impact_radius ** 2:
                    targets.append((i, j))

        # disable the targets
        for target in targets:
            pass
            # TODO: add event to disable the target

        return f'Throw EMP bomb at ({px}, {py})'
