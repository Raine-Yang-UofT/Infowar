import socket
import pickle


class Network:
    """
    Client-side network connection, connect a client to server
    """
    def __init__(self, server_ip: str):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server_ip  # the server's address, currently local address
        """
            Note: always check for correct server ip
        """
        self.port = 5555  # the port for connection
        self.addr = (self.server, self.port)
        self.player = None

    def get_player(self):
        """
        Get the player (client) object
        :return: the player object
        """
        return self.player

    def connect(self, robot_config) -> None:
        """
        connect client to server

        :param robot_config: the robot configuration loaded from client
        """
        try:
            self.client.connect(self.addr)  # connect client socket to server address
            self.client.send(pickle.dumps(robot_config))  # send robot configuration to server
            self.player = pickle.loads(self.client.recv(2048 * 4))     # receive Robot object from server
        except Exception as e:
            print(e)
            pass

    def send(self, data):
        """
        Send data to server and receive the server's response

        :param data: the data sent to server
        :return: the server's response
        """
        try:
            self.client.send(pickle.dumps(data))   # send client command
            self.player = pickle.loads(self.client.recv(2048 * 4))
            return self.player     # receive Robot object from server
        except socket.error as e:
            print(e)


