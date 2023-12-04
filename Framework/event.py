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

    def __lt__(self, other):
        """
        Compare two events by their start round

        :param other: the other event to compare
        :return: True if self < other, False otherwise
        """
        return self.start_round < other.start_round
