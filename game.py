"""
The class of a gameplay
"""
from battlefield import Battlefield
from robot import Robot
import message
from message import Message
from queue import PriorityQueue

# Game Configurations
FIELD_ROW = 15
FIELD_COL = 15
BARRICADE_COVERAGE = 0.4
HARD_BARRICADE_COVERAGE = 0.2
BARRICADE_HP_RANGE = (50, 200)
BARRICADE_ARMOR_RANGE = (1, 3)


class Game:

    def __init__(self, game_id: int, num_players: int) -> None:
        """
        Initialize a game with players and a battlefield

        :param game_id: the game_id assigned by server
        :param num_players: the number of players to start a game
        """
        self.game_id = game_id
        self.num_players = num_players
        self.battlefield = Battlefield(FIELD_ROW, FIELD_ROW)
        self.battlefield.initialize_field(BARRICADE_COVERAGE, HARD_BARRICADE_COVERAGE, BARRICADE_HP_RANGE,
                                          BARRICADE_ARMOR_RANGE)
        self.players = {}  # the dict of all players
        self.game_start = False  # whether the game as started

        # initialize message centers and controllers
        self.message_center = MessageCenter(self)
        self.move_controller = MoveController(self)

    def add_player(self, player: Robot, player_id: int) -> None:
        """
        Add a new player to the game field

        :param player: the player in the game
        :param player_id: the id of player
        :return: None
        """
        self.players[player_id] = player
        self.battlefield.initialize_player_location(player)
        # start the game when there are enough players
        if len(self.players) == self.num_players:
            self.game_start = True

    def get_player(self, player_id: int) -> Robot:
        """
        Return the corresponding player object with a given id

        Precondition:
            - player_id in players

        :param player_id: the id of player
        :return: the Robot object corresponding to player_id
        """
        return self.players[player_id]


class MessageCenter:
    """
    Store and distribute client commands
    """

    def __init__(self, game):
        """
        Initialize the message queue

        :param game: the game being played
        """
        self.message_queue = PriorityQueue()
        self.game = game

        self.num_players = game.num_players
        self.num_players_went = 0   # the number of players who made their moves
        self.complete_round = False    # whether all player moves have been executed

    def receive_message(self, player_message: Message) -> None:
        """
        receive a message from server and put it in the message queue

        :param player_message: the player message to receive
        :return: None
        """
        self.complete_round = False
        self.message_queue.put((player_message.priority, player_message))
        self.num_players_went += 1  # add one player who makes its move
        if self.num_players_went == self.num_players:   # execute messages when all players made action
            self.execute_commands()

    def execute_commands(self) -> None:
        """
        Process messages send by players and invoke corresponding methods
        in RobotController

        :return: None
        """
        self.num_players_went = 0   # reset player movement count

        while not self.message_queue.empty():
            player_message = self.message_queue.get()[1]
            # distribute the message to corresponding controllers
            if player_message.type == message.TYPE_MOVE:
                # send move message to MoveController
                self.game.move_controller.receive_message(player_message)
            # TODO Handle more message types
            else:
                print("Unidentified Message Type!")

        self.complete_round = True  # all player commands have been processed, time to send message to clients


class MoveController:
    """
    A controller class for players' movement in the field
    """

    def __init__(self, game: Game) -> None:
        """
        Initialize MoveController

        :param game: the game being played
        """
        self.game = game

    def receive_message(self, player_message: Message) -> None:
        """
        Receive a movement message from MessageCenter

        :param player_message: the message to execute
        :return: None
        """
        direction = player_message.data  # the direction of movement
        robot = self.game.players[player_message.source]    # the robot to control

        # cannot find robot position
        if robot.get_pos() is None:
            print("Cannot find the robot's current position")
            return

        x, y = robot.get_pos()  # the player's current location

        if direction == message.UP:
            self.move_player(robot, (x - 1, y))
        elif direction == message.DOWN:
            self.move_player(robot, (x + 1, y))
        elif direction == message.LEFT:
            self.move_player(robot, (x, y - 1))
        elif direction == message.RIGHT:
            self.move_player(robot, (x, y + 1))

    def move_player(self, robot, target_pos: tuple) -> None:
        """
        Move a player from original_pos to target_pos, and store the movement status
        into player's information list

        :param robot: the robot to move
        :param target_pos: the (x, y) coordinates of the player's destinated location
        :return: None
        """
        field = self.game.battlefield
        original_pos = robot.get_pos()
        print(original_pos)

        if field.is_blocked(target_pos[0], target_pos[1]):
            robot.receive_info("Movement failed, the location has been blocked")
            return

        # move the robot
        field.get_grid(target_pos[0], target_pos[1]).change_occupant(robot)
        field.get_grid(original_pos[0], original_pos[1]).change_occupant(None)
        robot.set_pos(field.get_grid(target_pos[0], target_pos[1]))
        robot.receive_info("Move to (" + str(robot.get_pos()[0]) + ", " + str(robot.get_pos()[1]) + ")")
        # generate sound and heat signal
        field.generate_sound(target_pos[0], target_pos[1], robot.move_sound)
        field.generate_heat(target_pos[0], target_pos[1], robot.move_heat)

