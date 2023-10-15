"""
The client end for communication
"""

from network import Network
from robot_config import RobotConfig
import message
from message import Message

if __name__ == '__main__':
    # TODO check robot config

    # TODO initial connection with server
    net = Network("100.67.81.159")
    net.connect(RobotConfig(100, 3))
    player = net.get_player()   # receive the initialized player robot
    print("You are player " + str(player.get_id()))
    print("Waiting for other players...")

    # receive starting message
    player = net.send(Message(message.TYPE_CONNECT, message.CONNECT, None, 0))
    print("Match found, start game...")
    print(player.display_status())

    # the game loop


