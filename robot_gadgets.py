"""
Handle gadget use
"""
import Framework.message as message
import barricade
from Items import gadgets
from Framework.event import Event


class RobotGadgets:

    def __init__(self, game) -> None:
        self.game = game
        self.battlefield = game.battlefield
        self.event_handler = game.event_handler

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

    def throw_EMP_bomb(self, x: int, y: int, gadget: gadgets.EMPBomb) -> []:
        """
        Throw an EMP bomb at a certain direction and range from (x, y)

        :param x: the x-coordinate of the starting point
        :param y: the y-coordinate of the starting point
        :param gadget: the EMP bomb to throw
        :return: result on throwing
        """
        px, py = x, y
        if gadget.direction == message.UP:
            py -= gadget.range
        elif gadget.direction == message.DOWN:
            py += gadget.range
        elif gadget.direction == message.LEFT:
            px -= gadget.range
        elif gadget.direction == message.RIGHT:
            px += gadget.range

        # generate sound and heat at starting position
        self.battlefield.generate_sound(x, y, gadget.config.sound_emission)
        self.battlefield.generate_heat(x, y, gadget.config.heat_emission)

        # find the targets in range
        targets = []
        from robot import Robot  # temporarily import robot
        for i in range(max(0, px - gadget.config.impact_radius), min(len(self.battlefield.field[0]), px + gadget.config.impact_radius + 1)):
            for j in range(max(0, py - gadget.config.impact_radius), min(len(self.battlefield.field), py + gadget.config.impact_radius + 1)):
                if (i - px) ** 2 + (j - py) ** 2 <= gadget.config.impact_radius ** 2:
                    occupant = self.battlefield.get_grid(i, j).get_occupant()
                    if isinstance(occupant, Robot):
                        targets.append("EMP bomb hit " + occupant.get_name() + '!')
                        # disable robot
                        occupant.states.set_state("move", False, 1)
                        occupant.states.set_state("sensor", False, 1)
                        occupant.states.set_state("weapon", False, 1)
                        occupant.states.set_state("gadget", False, 1)

        return targets
