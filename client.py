"""
The client end for communication
"""

from network import Network
from robot_config import RobotConfig, default_base
import message
from message import Message

if __name__ == '__main__':
    # TODO check robot config

    net = Network("100.67.87.52")
    net.connect(RobotConfig(default_base))
    player = net.get_player()   # receive the initialized player robot
    print("You are player " + str(player.get_id()))
    print("Waiting for other players...")

    # receive starting message
    # no player index available now, use 0 for placehold of "source" parameter
    player = net.send(Message(0, message.TYPE_CONNECT, message.CONNECT, None, 0))
    print("Match found, start game...")
    print(player.display_status())

    # the game loop
    while True:
        # TODO: read user input from command line
        # TODO: send command to server
        pass

