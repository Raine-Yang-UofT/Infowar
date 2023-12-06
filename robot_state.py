from dataclasses import dataclass


@dataclass
class State:
    """
    the class for a single robot state

        - state: the status of the state
        - recovery_time: the time before the state recovers to normal

    Note: 0 recovery_time indicates normal state, -1 indicates the state never recovers
    """
    state: bool
    recovery_time: int


class RobotState:

    def __init__(self):
        """
        the class for robot states

        The robot stores its state in a dictionary, with the following keys:

            - vision: whether the robot has vision
            - move: whether the robot can move
            - sensor: whether the robot can use sensors
            - weapon: whether the robot can use weapons
            - gadget: whether the robot can use gadgets
            - alive: whether the robot is alive
        """
        self.state = {"vision": State(True, 0), "move": State(True, 0), "sensor": State(True, 0),
                      "weapon": State(True, 0), "gadget": State(True, 0), "alive": State(True, 0)}

    def set_normal(self):
        """
        set the robot to normal state

        :return: None
        """
        for key in self.state:
            self.state[key] = State(True, 0)

    def set_dead(self):
        """
        set the robot to dead state

        :return: None
        """
        for key in self.state:
            self.state[key] = State(False, -1)

    def set_state(self, state_type: str, state: bool, recovery_time: int) -> None:
        """
        Set the state of robot

        Preconditions:
            - state_type in self.states ("vision", "move", "sensor", "weapon", "gadget", "alive")

        :param state_type: the type of state to set
        :param state: the state to set
        :param recovery_time: the recovery time of the state
        :return: None
        """
        self.state[state_type] = State(state, recovery_time)

    def update_state(self):
        """
        Update robot state after each round
        """
        for key in self.state:
            if self.state[key].recovery_time > 0:
                self.state[key].recovery_time -= 1
            elif self.state[key].recovery_time == 0:
                self.state[key].state = True
