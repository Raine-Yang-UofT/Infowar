"""
gadget items
"""
from dataclasses import dataclass, replace
from Framework import message, interface
from Framework import input_code


@dataclass(frozen=True)
class DeployableBarricadeConfig:
    """
    A hard barricade that can be deployed on the ground. It can block straight-firing weapons and robots

        - name: the name of the gadget
        - HP: the HP of the gadget
        - armor: the armor of the gadget
        - reaction_time: the reaction speed of gadget (determines message priority)
    """
    name: str
    HP: int
    armor: int
    reaction_time: int


class DeployableBarricade(interface.IGadget):
    """
    The deployable barricade gadget class
    """
    def __init__(self, config: DeployableBarricadeConfig):
        self.config = config
        self.message = -1

    def use_gadget(self, gadgets, robot) -> None:
        """
        Deploy a hard barricade at the current position of the robot

        :param gadgets: the RobotGadgets observer class
        :param robot: the robot that uses the gadget
        :return: None
        """
        robot.receive_info(gadgets.deploy_barricade(robot.get_pos()[0], robot.get_pos()[1], self))

    def select_gadget_parameter(self):
        """
        Select the direction to deploy the barricade

        :return: a copy of gadget object with updated parameters
        """
        command_input = input("Select the direction to deploy barricade:" +
                              input_code.UP + ": up  " + input_code.DOWN + ": down  " + input_code.LEFT + ": left  " + input_code.RIGHT + ": right")
        if command_input not in [input_code.UP, input_code.DOWN, input_code.LEFT, input_code.RIGHT]:
            raise input_code.InvalidCommandException()
        self.message = input_code.get_direction_message(command_input)
        return self  # update weapon message as firing direction


# gadget objects
deployable_barricade = DeployableBarricade(DeployableBarricadeConfig('deployable barricade', 200, 5, 10))
