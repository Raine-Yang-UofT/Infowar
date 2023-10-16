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


if __name__ == '__main__':
    game = Game(0)
    player0 = Robot(RobotConfig(default_base), 0)
    player1 = Robot(RobotConfig(default_base), 1)
    player2 = Robot(RobotConfig(default_base), 2)

    game.add_player(player0, 0, 3)
    game.add_player(player1, 1, 3)
    game.add_player(player2, 2, 3)

    print_field(game.battlefield)
    print()

    message_center = MessageCenter(game)
    message_center.receive_message(Message(0, message.TYPE_MOVE, message.MOVE, message.UP, 0))
    message_center.execute_commands()
    print_field(game.battlefield)
    player0.print_info()

    print_sound(game.battlefield)


