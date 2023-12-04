from dataclasses import dataclass


@dataclass
class Event:
    """
    A event to be executed in multiple round

        - start_round: the round to start
        - end_round: the round to end
        - callback: the callback function to execute
    """
    start_round: int
    end_round: int
    callback: callable
