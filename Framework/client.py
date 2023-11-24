"""
The client end for communication
"""
import sys
import os
from dataclasses import replace

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


class InvalidCommandException(Exception):

    def __str__(self):
        return 'Invalid Command'


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
        sensor = select_sensor_parameters(player.sensors[index])  # input additional parameters for sensor
    except Exception as e:  # prevent invalid index
        print("Invalid Command")
        print(e)
        return None

    # send message
    # sensors always have the lowest priority
    return net.send(Message(net.get_player().get_id(), message.TYPE_SENSE, sensor.message, sensor, INFINITY))


def select_sensor_parameters(sensor):
    """
    Prompt player to add paramters to sensor command (is required)

    :param sensor: the sensor dataclass
    :return: a new sensor object
    """
    if sensor.message == message.SENSE_DRONE:
        command = input("Enter (w, a, s, d) to map the path of drone: ")
        if not (all([c in ['w', 'a', 's', 'd'] for c in command]) and len(command) <= sensor.longest_range):
            print("Invalid drone path, make sure the path only contains (w, a, s, d) and is shorter than " + str(
                sensor.longest_range) + " steps")
            raise InvalidCommandException()
        # update drone path
        print("drone path updated")
        return replace(sensor, commands=command)
    elif sensor.message == message.SENSE_SCOUT_CAR:
        direction = input("Enter (w, a, s, d) to map the direction of scout car: ")
        if direction not in ['w', 'a', 's', 'd']:
            print("Invalid scout car direction, make sure the direction is one of (w, a, s, d)")
            raise InvalidCommandException()
        # update scout car direction
        print("scout car direction updated")
        return replace(sensor, direction=direction)
    else:
        # no additional parameters for sensors
        return sensor


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
        weapon = select_weapon_parameters(player.weapons[index])  # input additional parameters for weapon
    except Exception as e:  # prevent invalid index
        print("Invalid Command")
        print(e)
        return None

    # send message
    # calculate priority: 100 - weapon.reaction_time
    return net.send(Message(net.get_player().get_id(), message.TYPE_FIRE, weapon.message, weapon,
                            max(0, 100 - weapon.reaction_time)))


def select_weapon_parameters(weapon):
    """
    Prompt player to add paramters to weapon command (is required)

    :param weapon: the weapon selected
    :return: the updated weapon
    """
    # select direction for straight-firing weapons
    if isinstance(weapon, weapons.StraightWeapon):
        command_input = input("Select the direction of firing:" +
                              input_code.UP + ": up  " + input_code.DOWN + ": down  " + input_code.LEFT + ": left  " + input_code.RIGHT + ": right")
        if command_input not in [input_code.UP, input_code.DOWN, input_code.LEFT, input_code.RIGHT]:
            raise InvalidCommandException()
        return replace(weapon, message=get_direction_message(command_input))  # update weapon message as firing direction
    elif isinstance(weapon, weapons.ProjectileWeapon):
        command_input = input("Select the direction of firing:" +
                              input_code.UP + ": up  " + input_code.DOWN + ": down  " + input_code.LEFT + ": left  " + input_code.RIGHT + ": right")
        range_input = input(
            "Select the range of firing: (range between " + str(weapon.min_launch_range) + " - " + str(
                weapon.max_launch_range) + ")")
        if range_input.isdigit():
            range_input = int(range_input)
        else:
            raise InvalidCommandException()

        if ((command_input not in [input_code.UP, input_code.DOWN, input_code.LEFT, input_code.RIGHT])
                or range_input < weapon.min_launch_range or range_input > weapon.max_launch_range):
            raise InvalidCommandException()
        return replace(weapon, message=(get_direction_message(command_input), range_input))  # update weapon message as firing direction and range
    else:
        # no additional parameters for weapons
        return weapon


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

    net = Network("100.67.90.173")
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
