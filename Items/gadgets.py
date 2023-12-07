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
class ProjectileGadgetConfig:
    """
    A gadget that can be thrown as a projectile

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


class ProjectileGadget(interface.IGadget):
    """
    The projectile gadget class
    Projectile gadgets can be thrown to a certain location and causes certain effect

    :param config: the configuration of the gadget
    :param execution_function: the function to execute the gadget
    """
    def __init__(self, config: ProjectileGadgetConfig, execution_function):
        self.config = config
        self.remain = config.total_use
        self.total = config.total_use
        self.execution_function = execution_function
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
        results = gadgets.throw_projectile_gadget(robot.get_pos()[0], robot.get_pos()[1], self)
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
            raise input_code.InvalidCommandException(f"No remaining use of {self.config.name}")

        return prompt.select_direction_and_range(self, f"Select the direction to throw {self.config.name}:", f"Select the range to throw {self.config.name}:")

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
class RepairKitConfig:
    """
    A gadget that can recover HP and armor

            - name: the name of gadget
            - HP: the HP recovered
            - armor: the armor recovered
            - reaction_time: the reaction speed of gadget (determines message priority)
            - total_use: the total number of times the gadget can be used
    """
    name: str
    HP: int
    armor: int
    reaction_time: int
    total_use: int


class RepairKit(interface.IGadget):
    """
    The repair kit gadget class
    """
    def __init__(self, config: RepairKitConfig):
        self.config = config
        self.remain = config.total_use
        self.total = config.total_use

    def use_gadget(self, gadgets, robot) -> None:
        """
        Use a repair kit

        :param gadgets: the RobotGadgets observer class
        :param robot: the robot that uses the gadget
        :return: None
        """
        self.remain -= 1
        robot.receive_info(gadgets.use_repair_kit(robot, self))

    def select_gadget_parameter(self):
        """
        Select the direction to use the repair kit

        :return: a copy of gadget object with updated parameters
        """
        # check remaining use
        if not self.check_remaining_use():
            raise input_code.InvalidCommandException("No remaining use of repair kit")
        return self  # no additional parameters

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
        total_use=3
    )
)


# the effects of EMP bomb
def EMP_effect(target):
    target.states.set_state("move", False, 1)
    target.states.set_state("sensor", False, 1)
    target.states.set_state("weapon", False, 1)
    target.states.set_state("gadget", False, 1)


EMP_bomb = ProjectileGadget(
    ProjectileGadgetConfig(
        name='EMP bomb',
        min_launch_range=3,
        max_launch_range=8,
        impact_radius=2,
        sound_emission=3,
        heat_emission=3,
        reaction_time=80,
        total_use=2
    ),
    execution_function=EMP_effect
)


# the effects of flash bomb
def flash_effect(target):
    target.states.set_state("vision", False, 2)
    target.states.set_state("sensor", False, 2)
    target.states.set_state("weapon", False, 1)


flash_bomb = ProjectileGadget(
    ProjectileGadgetConfig(
        name='flash bomb',
        min_launch_range=4,
        max_launch_range=6,
        impact_radius=3,
        sound_emission=6,
        heat_emission=5,
        reaction_time=80,
        total_use=2
    ),
    execution_function=flash_effect
)


repair_kit = RepairKit(
    RepairKitConfig(
        name='repair kit',
        HP=25,
        armor=1,
        reaction_time=10,
        total_use=1
    )
)
