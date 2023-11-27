"""
gadget items
"""
from dataclasses import dataclass
from Framework import message


@dataclass(frozen=True)
class DeployableBarricade:
    """
    A hard barricade that can be deployed on the ground. It can block straight-firing weapons and robots

        - name: the name of the gadget
        - HP: the HP of the gadget
        - armor: the armor of the gadget
        - message: the message associated with the gadget
        - reaction_time: the reaction speed of gadget (determines message priority)
    """
    name: str
    HP: int
    armor: int
    message: int
    reaction_time: int

    def use_gadget(self, gadgets, robot) -> None:
        """
        Deploy a hard barricade at the current position of the robot

        :param gadgets: the RobotGadgets observer class
        :param robot: the robot that uses the gadget
        :return: None
        """
        robot.receive_info(gadgets.deploy_barricade(robot.get_pos()[0], robot.get_pos()[1], self))


# gadget objects
deployable_barricade = DeployableBarricade('deployable barricade', 200, 5, message.DEPLOYABLE_BARRICADE, 10)
