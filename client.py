"""
The client end for communication
"""

from network import Network
from robot_config import RobotConfig, default_base
import message
from message import Message
import input_code


def select_move_command(net: Network):
    """
    Prompt the player to send movement command

    :param net: the network connection to server
    :return: the robot object received from server
    """
    print("Select the direction of movement")
    command_input = input(input_code.UP + ": up  " + input_code.DOWN + ": down  " + input_code.LEFT + ": left  " + input_code.RIGHT + ": right")

    # invalid command
    if command_input not in [input_code.UP, input_code.DOWN, input_code.LEFT, input_code.RIGHT]:
        print("Invalid Command")
        return None

    # send message
    direction = get_direction_message(command_input)
    return net.send(Message(net.get_player().get_id(), message.TYPE_MOVE, message.MOVE, direction, move_speed))


def get_direction_message(command_input: str) -> int:
    """
    Return the corresponding message code for directions from input code
    Return -1 if no corresponding code found

    :param command_input: the input code
    :return: corresponding message code
    """
    if command_input == input_code.UP:
        return message.UP
    elif command_input == input_code.DOWN:
        return message.DOWN
    elif command_input == input_code.LEFT:
        return message.LEFT
    elif command_input == input_code.RIGHT:
        return message.RIGHT

    return -1


if __name__ == '__main__':
    # TODO check robot config
    move_speed = 50
    # TODO assign the veriables about by configuration

    net = Network("100.67.82.133")
    net.connect(RobotConfig(default_base))
    player = net.get_player()   # receive the initialized player robot
    print("You are player " + str(player.get_id()))
    print("Waiting for other players...")

    # receive starting message
    # no player index available now, use 0 for placehold of "source" parameter
    player = net.send(Message(0, message.TYPE_CONNECT, message.CONNECT, None, 0))
    print("Match found, start game...")
    round_count = 0  # count the number of rounds taken place

    # the game loop
    while True:
        # TODO: read user input from command line
        round_count += 1
        # print robot status and information
        print(player.display_status())
        player.print_info()
        print("Map: ")
        player.print_map()

        print("Round " + str(round_count) + "  Please select your move:")

        # get player input
        valid_command = False
        command_type = ''
        while not valid_command:
            command_type = input(input_code.MOVE + ": move  " + input_code.SENSE + ": sense  " + input_code.FIRE + ": fire  " + input_code.GADGET + " gadget")
            if command_type == input_code.MOVE:    # receive movement command
                player = select_move_command(net)
                if player is not None:
                    valid_command = True    # successfully received server response
            else:
                print("Invalid Command")

        print('-' * 30)
