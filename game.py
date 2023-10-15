"""
The class of a gameplay
"""
from battlefield import Battlefield
from robot import Robot

# Game Configurations
FIELD_ROW = 15
FIELD_COL = 15
BARRICADE_COVERAGE = 0.4
HARD_BARRICADE_COVERAGE = 0.2
BARRICADE_HP_RANGE = (50, 200)
BARRICADE_ARMOR_RANGE = (1, 3)


class Game:

    def __init__(self, game_id: int) -> None:
        """
        Initialize a game with players and a battlefield

        :param game_id: the game_id assigned by server
        """
        self.game_id = game_id
        self.battlefield = Battlefield(FIELD_ROW, FIELD_ROW)
        self.battlefield.initialize_field(BARRICADE_COVERAGE, HARD_BARRICADE_COVERAGE, BARRICADE_HP_RANGE, BARRICADE_ARMOR_RANGE)
        self.players = {}   # the dict of all players
        self.game_start = False  # whether the game as started

    def add_player(self, player: Robot, player_id: int, num_players: int) -> None:
        """
        Add a new player to the game field

        :param player: the player in the game
        :param player_id: the id of player
        :param num_players: the number of players to start a game
        :return: None
        """
        self.players[player_id] = player
        self.battlefield.initialize_player_location(player)
        print(self.battlefield.display())
        # start the game when there are enough players
        if len(self.players) == num_players:
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

