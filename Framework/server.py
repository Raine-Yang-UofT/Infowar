import socket
from _thread import *
import pickle

from robot import Robot
from game import Game
import message

server = "100.71.95.110"  # the server's address, currently local address
port = 5555  # the port for connection

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# initialze the server
try:
    server_socket.bind((server, port))  # bind the server and the port
except socket.error as e:
    str(e)  # print socket error message

# wait for client connection
NUM_PLAYERS = 3  # the numbere of players in each game
server_socket.listen(NUM_PLAYERS)  # listen for connection, param: the maximum connection accepted

games = {}  # store games id(int): Game
id_count = 0  # the total number of client threads created


def threaded_client(conn, player_id: int, game_id: int):
    """
    Start a new thread to handle a player.

    :param conn: the client connection
    :param player_id: the player's id
    :param game_id: the id of the player
    :return: None
    """
    global games
    current_game = games[game_id]
    print("start new thread")

    # receive robot configuration
    config = pickle.loads(conn.recv(2048 * 4))
    player = Robot(config, player_id)
    current_game.add_player(player, player_id)  # add player to field
    conn.send(pickle.dumps(player))

    # wait for all players to connect
    while not current_game.game_start:
        pass

    # send client's robot when all players join the game
    if pickle.loads(conn.recv(2048)).type == message.TYPE_CONNECT:
        conn.send(pickle.dumps(current_game.get_player(player_id)))

    # the game loop
    while True:
        try:
            # receive client message
            client_message = pickle.loads(conn.recv(2048 * 4))  # read client command
            current_game.message_center.receive_message(client_message)  # add message to message center
            print("receive client message")

            # wait until every player made their moves
            while not current_game.message_center.complete_round:
                pass

            # send client status
            print("finish processing commands, send client status")
            current_game.update_player_map(current_game.get_player(player_id))  # update the robot local map
            conn.send(pickle.dumps(current_game.get_player(player_id)))

            # update game
            current_game.reset_game_update()
        except Exception as exception:  # cannot receive client message
            print(exception)
            break


while True:
    conn, addr = server_socket.accept()
    print("connect to " + str(addr))

    id_count += 1
    game_id = (id_count - 1) // NUM_PLAYERS   # match players to a game
    player_id = 1   # the id of each player, from 1 to num_players
    if id_count % NUM_PLAYERS == 1:  # start a new game
        games[game_id] = Game(game_id, NUM_PLAYERS)  # create new game
        print("Creating a new game...")
    else:   # join the player in an existing game
        player_id = id_count % NUM_PLAYERS

    start_new_thread(threaded_client, (conn, player_id, game_id))  # assign a new thread to handle player
