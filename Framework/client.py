"""
The client end for communication
"""

from network import Network
from Configurations.robot_config import default_config, RobotConfig
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
    command_input = input(
        input_code.UP + ": up  " + input_code.DOWN + ": down  " + input_code.LEFT + ": left  " + input_code.RIGHT + ": right")

    # invalid command
    if command_input not in [input_code.UP, input_code.DOWN, input_code.LEFT, input_code.RIGHT]:
        print("Invalid Command")
        return None

    # send message
    direction = get_direction_message(command_input)
    return net.send(Message(net.get_player().get_id(), message.TYPE_MOVE, message.MOVE, direction, player.move_speed))


def select_sense_command(net: Network):
    """
    Prompt the player to send sense command

    :param net: the network connection to server
    :return: the robot object received from server
    """
    print("Select the sensor")
    prompt = ''
    for i in range(0, len(player.sensors)):
        prompt += str(i + 1) + ": " + player.sensors[i].name + "  "
    try:
        index = int(input(prompt)) - 1
        sensor = player.sensors[index]
    except:  # prevent invalid index
        print("Invalid Command")
        return None

    # send message
    return net.send(Message(net.get_player().get_id(), message.TYPE_SENSE, sensor.message, sensor, 0))

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
    # TODO check the validity of robot config

    net = Network("100.71.95.110")
    net.connect(default_config)
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
        round_count += 1
        # print robot status and information
        print(player.display_status())
        player.print_info()
        player.print_vision()
        print("Map: ")
        player.print_map()

        print("Round " + str(round_count) + "  Please select your move:")

        # get player input
        valid_command = False
        command_type = ''
        result = None
        while not valid_command:
            command_type = input(
                input_code.MOVE + ": move  " + input_code.SENSE + ": sense  " + input_code.FIRE + ": fire  " + input_code.GADGET + " gadget")
            if command_type == input_code.MOVE:    # receive movement command
                result = select_move_command(net)
            elif command_type == input_code.SENSE:  # receive sensor command
                result = select_sense_command(net)
            else:
                print("Invalid Command")
            if result is not None:
                valid_command = True  # successfully received server response
                player = result  # update player

        print('-' * 30)
