"""
Handle gadget use
"""
from battlefield import Battlefield
import Items.gadgets as gadgets
import Framework.message as message
import barricade


class RobotGadgets:

    def __init__(self, field: Battlefield):
        self.battlefield = field

    def deploy_barricade(self, x: int, y: int, gadget) -> str:
        """
        Deploy a hard barricade at a certain direction from (x, y)

        :param x: the x-coordinate of the deployment point
        :param y: the y-coordinate of the deployment point
        :param gadget: the hard barricade to deploy
        :return: result on deployment
        """
        px, py = x, y
        if gadget.message == message.UP:
            py -= 1
        elif gadget.message == message.DOWN:
            py += 1
        elif gadget.message == message.LEFT:
            px -= 1
        elif gadget.message == message.RIGHT:
            px += 1

        if self.battlefield.is_blocked(px, py):
            return 'Deployment failed: the location has been blocked'

        grid = self.battlefield.get_grid(px, py)
        grid.change_occupant(barricade.HardBarricade(gadget.HP, gadget.armor, grid))

        return f'Deploy barricade at ({px}, {py})'
