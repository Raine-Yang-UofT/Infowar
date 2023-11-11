"""
The class of a gameplay
"""
from battlefield import Battlefield
from robot import Robot
from Framework import message
from Framework.message import Message
from queue import PriorityQueue
from Configurations import game_config
from robot_sensors import RobotSensor


class Game:

    def __init__(self, game_id: int, num_players: int) -> None:
        """
        Initialize a game with players and a battlefield

        :param game_id: the game_id assigned by server
        :param num_players: the number of players to start a game
        """
        self.game_id = game_id
        self.num_players = num_players
        self.battlefield = Battlefield(game_config.FIELD_ROW, game_config.FIELD_COL)
        self.sensors = RobotSensor(self.battlefield)
        self.battlefield.initialize_field(game_config.BARRICADE_COVERAGE, game_config.HARD_BARRICADE_COVERAGE, game_config.BARRICADE_HP_RANGE,
                                          game_config.BARRICADE_ARMOR_RANGE)
        self.players = {}  # the dict of all players
        self.game_start = False  # whether the game as started
        self.game_update_counter = 0  # how many threads finish the round

        # initialize message centers and controllers
        self.message_center = MessageCenter(self)
        self.move_controller = MoveController(self)
        self.sensor_controller = SensorController(self)

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

    def update_game(self) -> None:
        """
        Update game after each round

        Reduce sound and heat intensity
        Reset robot info_list
        Reset robot vision

        :return: None
        """
        self.battlefield.reduce_sound_and_heat(game_config.SOUND_REDUCTION, game_config.HEAT_REDUCTION)

        for player_id in self.players:
            # clear information list
            self.players[player_id].clear_info()
            self.players[player_id].vision = []

        print_field(self.battlefield)   # test method: print field
        print('---')
        print_sound(self.battlefield)
        print('---')
        print_heat(self.battlefield)

    def reset_game_update(self) -> None:
        """
        Notify that one thread has finished sending client message,
        Reset self.game_update to False when all threads finish

        :return: None
        """
        self.game_update_counter += 1
        if self.game_update_counter == self.num_players:
            self.update_game()
            self.game_update_counter = 0  # reset counter

    def update_player_map(self, robot) -> None:
        """
        Update the map of a robot

        :param robot: the robot to update
        :return: None
        """
        x, y = robot.get_pos()
        robot.update_map(self.sensors.display_player_vision(x, y))


# test methods: print battlefield status to terminal
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
            elif player_message.type == message.TYPE_SENSE:
                self.game.sensor_controller.receive_message(player_message)
            # TODO Handle more message types
            else:
                print("Unidentified Message Type!")

        print('complete round')
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
            self.move_player(robot, (x, y - 1))
        elif direction == message.DOWN:
            self.move_player(robot, (x, y + 1))
        elif direction == message.LEFT:
            self.move_player(robot, (x - 1, y))
        elif direction == message.RIGHT:
            self.move_player(robot, (x + 1, y))

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


class SensorController:
    """
    A controller class for sensors
    """
    def __init__(self, game: Game) -> None:
        """
        Initialize MoveController

        :param game: the game being played
        """
        self.game = game

    def receive_message(self, player_message: Message) -> None:
        """
        Receive a sensor message from MessageCenter

        :param player_message: the player message to be executed
        :return: None
        """
        sensor = player_message.data  # the sensor object class
        robot = self.game.players[player_message.source]    # the robot to control

        if sensor.message == message.SENSE_SOUND:  # get the sound signal
            sound_signal = self.game.sensors.display_signal_vision(robot.get_pos()[0], robot.get_pos()[1], 'sound', sensor.radius)
            robot.receive_info("Sound signal detected at (" + str(robot.get_pos()[0]) + ", " + str(robot.get_pos()[1]) + ")")
            robot.receive_info("Sound signal: ")
            robot.receive_info(sound_signal)
        elif sensor.message == message.SENSE_HEAT:
            # get the heat signal
            heat_signal = self.game.sensors.display_signal_vision(robot.get_pos()[0], robot.get_pos()[1], 'heat', sensor.radius)
            robot.receive_info("Heat signal detected at (" + str(robot.get_pos()[0]) + ", " + str(robot.get_pos()[1]) + ")")
            robot.receive_info("Heat signal: ")
            robot.receive_info(heat_signal)
        else:  # TODO: add more sensor types
            print("unidentified sensor type")
