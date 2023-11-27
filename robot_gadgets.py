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
        Deploy a hard barricade at (x, y)

        :param x: the x-coordinate of the deployment point
        :param y: the y-coordinate of the deployment point
        :param gadget: the hard barricade to deploy
        :return: result on deployment
        """
        if self.battlefield.is_blocked(x, y):
            return 'Deployment failed: the location has been blocked'

        grid = self.battlefield.get_grid(x, y)
        grid.change_occupant(barricade.HardBarricade(gadget.HP, gadget.armor, grid))

        return f'Deployed barricade at ({x}, {y})'
