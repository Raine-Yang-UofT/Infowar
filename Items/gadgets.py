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

    # TODO: implement gadget method
