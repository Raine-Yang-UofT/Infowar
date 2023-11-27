"""
The client end for communication
"""
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
sys.path.append(os.path.join(parent_dir, 'Configurations'))
sys.path.append(os.path.join(parent_dir, 'Items'))

from network import Network
from Configurations.robot_config import default_config
import message
from message import Message
import input_code
from Items import weapons

INFINITY = 1000000000  # a psudo-infinity value for sensor priority


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
    direction = input_code.get_direction_message(command_input)
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
        sensor = player.sensors[index].select_sensor_parameter()  # input additional parameters for sensor
    except Exception as e:  # prevent invalid index
        print("Invalid Command")
        print(e)
        return None

    # send message
    # sensors always have the lowest priority
    return net.send(Message(net.get_player().get_id(), message.TYPE_SENSE, sensor.message, sensor, INFINITY))


def select_fire_command(net: Network):
    """
    Prompt the player to send fire command

    :param net: the network connection to server
    :return: the robot object received from server
    """
    print("Select the weapon")
    prompt = ''
    for i in range(0, len(player.weapons)):
        prompt += str(i + 1) + ": " + player.weapons[i].name + "  "
    try:
        index = int(input(prompt)) - 1
        weapon = player.weapons[index].select_weapon_parameter()  # input additional parameters for weapon
    except Exception as e:  # prevent invalid index
        print("Invalid Command")
        print(e)
        return None

    # send message
    # calculate priority: 100 - weapon.reaction_time
    return net.send(Message(net.get_player().get_id(), message.TYPE_FIRE, weapon.message, weapon,
                            max(0, 100 - weapon.reaction_time)))


if __name__ == '__main__':
    # TODO check the validity of robot config

    net = Network("100.67.80.163")
    net.connect(default_config)
    player = net.get_player()  # receive the initialized player robot
    print("You are player " + str(player.get_id()))
    print("Waiting for other players...")

    # receive starting message
    # no player index available now, use 0 for placehold of "source" parameter
    player = net.send(Message(0, message.TYPE_CONNECT, message.CONNECT, None, 0))
    print("Match found, start game...")
    round_count = 0  # count the number of rounds taken place

    # the game loop
    while True:
        # end client if game is over
        if player.HP <= 0:
            print("You are dead, game over")
            # send disconnect message to server
            net.send(Message(net.get_player().get_id(), message.TYPE_DISCONNECT, message.DISCONNECT, None, -1))
            break

        round_count += 1
        # print robot status and information
        print(player.display_status())
        print("Information: ")
        player.print_info()
        print("Vision: ")
        player.print_vision()
        print("Round " + str(round_count) + "  Please select your move:")

        # get player input
        valid_command = False
        command_type = ''
        result = None
        while not valid_command:
            command_type = input(
                input_code.MOVE + ": move  " + input_code.SENSE + ": sense  " + input_code.FIRE + ": fire  " + input_code.GADGET + " gadget" + "   (m: display map)")
            if command_type == input_code.MOVE:  # receive movement command
                result = select_move_command(net)
            elif command_type == input_code.SENSE:  # receive sensor command
                result = select_sense_command(net)
            elif command_type == input_code.FIRE:  # receive fire command
                result = select_fire_command(net)
            elif command_type == 'm':  # open map
                print("Map: ")
                player.print_map()
            else:
                print("Invalid Command")
            if result is not None:
                valid_command = True  # successfully received server response
                player = result  # update player

        print('-' * 30)
