from battlefield import Battlefield
from game import Game, MessageCenter, MoveController
from robot import Robot
from robot_config import RobotConfig, default_base
import message
from message import Message


# test method: print the battlefield information on console
def print_field(b):
    for i in range(len(b.field)):
        for j in range(len(b.field[0])):
            print(b.field[i][j].display(), end="  ")
        print()  # Move to the next row


def print_sound(b):
    for i in range(len(b.field)):
        for j in range(len(b.field[0])):
            print(b.field[i][j].get_sound(), end="  ")
        print()  # Move to the next row


def print_heat(b):
    for i in range(len(b.field)):
        for j in range(len(b.field[0])):
            print(b.field[i][j].get_heat(), end="  ")
        print()  # Move to the next row


def print_list(b):
    for i in range(len(b)):
        for j in range(len(b[0])):
            print(b[i][j], end="  ")
        print()


if __name__ == '__main__':
    game = Game(0, 3)
    player0 = Robot(RobotConfig(default_base), 0)
    player1 = Robot(RobotConfig(default_base), 1)
    player2 = Robot(RobotConfig(default_base), 2)

    game.add_player(player0, 0)
    game.add_player(player1, 1)
    game.add_player(player2, 2)

    print_field(game.battlefield)
    print()

    print_list(game.battlefield.display_player_vision(player0.get_pos()[0], player0.get_pos()[1]))
    player0.update_map(game.battlefield.display_player_vision(player0.get_pos()[0], player0.get_pos()[1]))
    message_center = MessageCenter(game)
    message_center.receive_message(Message(0, message.TYPE_MOVE, message.MOVE, message.RIGHT, 0))
    message_center.execute_commands()
    print_field(game.battlefield)
    print_list(game.battlefield.display_player_vision(player0.get_pos()[0], player0.get_pos()[1]))
    player0.update_map(game.battlefield.display_player_vision(player0.get_pos()[0], player0.get_pos()[1]))
    player0.print_info()
    print_list(player0.map)
    print_sound(game.battlefield)



