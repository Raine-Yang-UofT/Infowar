"""
gadget items
"""
from dataclasses import dataclass
from Framework import interface
from Framework import input_code
from Items import prompt_template as prompt


@dataclass(frozen=True)
class DeployableBarricadeConfig:
    """
    A hard barricade that can be deployed on the ground. It can block straight-firing weapons and robots

        - name: the name of the gadget
        - HP: the HP of the gadget
        - armor: the armor of the gadget
        - reaction_time: the reaction speed of gadget (determines message priority)
        - total_use: the total number of times the gadget can be used
    """
    name: str
    HP: int
    armor: int
    reaction_time: int
    total_use: int


class DeployableBarricade(interface.IGadget):
    """
    The deployable barricade gadget class
    """
    def __init__(self, config: DeployableBarricadeConfig):
        self.config = config
        self.remain = config.total_use
        self.total = config.total_use
        self.direction = -1

    def use_gadget(self, gadgets, robot) -> None:
        """
        Deploy a hard barricade at the current position of the robot

        :param gadgets: the RobotGadgets observer class
        :param robot: the robot that uses the gadget
        :return: None
        """
        self.remain -= 1
        robot.receive_info(gadgets.deploy_barricade(robot.get_pos()[0], robot.get_pos()[1], self))

    def select_gadget_parameter(self):
        """
        Select the direction to deploy the barricade

        :return: a copy of gadget object with updated parameters
        """
        # check remaining use
        if not self.check_remaining_use():
            raise input_code.InvalidCommandException("No remaining use of deployable barricade")
        return prompt.select_direction(self, "Select the direction to deploy barricade:")

    def check_remaining_use(self) -> bool:
        """
        Check the remaining use of the gadget

        :return: whether there is remaining gadget use
        """
        return self.remain > 0

    def reset_remaining_use(self) -> None:
        """
        Reset the remaining use of the gadget

        :return: None
        """
        self.remain = self.total


@dataclass(frozen=True)
class EMPBombConfig:
    """
    An EMP bomb that can be thrown to temporarily disable robots in a range

        - name: the name of gadget
        - min_launch_range: the minimum range to launch gadget
        - max_launch_range: the maximum range to launch gadget
        - impact_radius: the impact radius (circular) of gadget
        - sound_emission: the sound emission of the gadget
        - heat_emission: the heat emission of the gadget
        - reaction_time: the reaction speed of gadget (determines message priority)
        - total_use: the total number of times the gadget can be used
    """
    name: str
    min_launch_range: int
    max_launch_range: int
    impact_radius: int
    sound_emission: int
    heat_emission: int
    reaction_time: int
    total_use: int


class EMPBomb(interface.IGadget):
    """
    The EMP bomb gadget class
    """
    def __init__(self, config: EMPBombConfig):
        self.config = config
        self.remain = config.total_use
        self.total = config.total_use
        self.direction = -1
        self.range = -1

    def use_gadget(self, gadgets, robot) -> None:
        """
        Throw an EMP bomb from robot

        :param gadgets: the RobotGadgets observer class
        :param robot: the robot that uses the gadget
        :return: None
        """
        self.remain -= 1
        results = gadgets.throw_EMP_bomb(robot.get_pos()[0], robot.get_pos()[1], self)
        if results is not None:
            for info in results:
                robot.receive_info(info)

    def select_gadget_parameter(self):
        """
        Select the direction to throw the EMP bomb

        :return: a copy of gadget object with updated parameters
        """
        # check remaining use
        if not self.check_remaining_use():
            raise input_code.InvalidCommandException("No remaining use of EMP bomb")

        return prompt.select_direction_and_range(self, "Select the direction to throw EMP bomb:", "Select the range to throw EMP bomb:")

    def check_remaining_use(self) -> bool:
        """
        Check the remaining use of the gadget

        :return: whether there is remaining gadget use
        """
        return self.remain > 0

    def reset_remaining_use(self) -> None:
        """
        Reset the remaining use of the gadget

        :return: None
        """
        self.remain = self.total


# gadget objects
deployable_barricade = DeployableBarricade(
    DeployableBarricadeConfig(
        name='deployable barricade',
        HP=200,
        armor=5,
        reaction_time=10,
        total_use=4
    )
)

EMP_bomb = EMPBomb(
    EMPBombConfig(
        name='EMP bomb',
        min_launch_range=3,
        max_launch_range=8,
        impact_radius=2,
        sound_emission=3,
        heat_emission=3,
        reaction_time=80,
        total_use=3
    )
)

