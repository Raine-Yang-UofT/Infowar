"""
A list of keyboard inputs

You can customize input by changing input codes, but make sure each variable
is assigned to a unique key
"""
import message

# input command type
MOVE = '1'
SENSE = '2'
FIRE = '3'
GADGET = '4'

# input direction
UP = 'w'
LEFT = 'a'
DOWN = 's'
RIGHT = 'd'


def get_direction_message(command_input: str) -> int:
    """
    Return the corresponding message code for directions from input code
    Return -1 if no corresponding code found

    :param command_input: the input code
    :return: corresponding message code
    """
    if command_input == UP:
        return message.UP
    elif command_input == DOWN:
        return message.DOWN
    elif command_input == LEFT:
        return message.LEFT
    elif command_input == RIGHT:
        return message.RIGHT

    return -1


class InvalidCommandException(Exception):

    def __str__(self):
        return 'Invalid Command'
