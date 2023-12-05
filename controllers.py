from Framework import message


class MoveController:
    """
    A controller class for players' movement in the field
    """

    def __init__(self, game) -> None:
        """
        Initialize MoveController

        :param game: the game being played
        """
        self.game = game

    def receive_message(self, player_message: message.Message) -> None:
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

        # check robot state
        if not robot.get_state().move:
            print("The robot's movement is interrupted!")
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
    def __init__(self, game) -> None:
        """
        Initialize SensorController

        :param game: the game being played
        """
        self.game = game

    def receive_message(self, player_message: message.Message) -> None:
        """
        Receive a sensor message from MessageCenter

        :param player_message: the player message to be executed
        :return: None
        """
        sensor = player_message.data  # the sensor object
        robot = self.game.players[player_message.source]    # the robot to control

        # check robot state
        if not robot.get_state().sensor:
            robot.receive_info("The robot's sensor is interrupted!")
            return

        # use the sensor
        sensor.detect_signal(self.game.sensors, robot)

        # update sensor to robot
        robot.sensors[player_message.command] = sensor


class WeaponController:
    """
    A controller class for weapons
    """
    def __init__(self, game):
        """
        Initialize WeaponController

        :param game: the game being played
        """
        self.game = game

    def receive_message(self, player_message: message.Message) -> None:
        """
        Receive a weapon message from MessageCenter

        :param player_message: the player message to be executed
        :return: None
        """
        weapon = player_message.data  # the weapon object
        robot = self.game.players[player_message.source]    # the robot to control

        # check robot state
        if not robot.get_state().weapon:
            robot.receive_info("The robot's weapon is interrupted!")
            return

        weapon.fire_weapon(self.game.weapons, robot)

        # update weapon to robot
        robot.weapons[player_message.command] = weapon


class GadgetController:
    """
    A controller class for gadgets
    """

    def __init__(self, game):
        """
        Initialize GadgetController

        :param game: the game being played
        """
        self.game = game

    def receive_message(self, player_message: message.Message) -> None:
        """
        Receive a gadget message from MessageCenter

        :param player_message: the player message to be executed
        :return: None
        """
        robot = self.game.players[player_message.source]    # the robot to control
        gadget = player_message.data  # the gadget object

        # check robot state
        if not robot.get_state().gadget:
            robot.receive_info("The robot's gadget is interrupted!")
            return

        # use gadget
        gadget.use_gadget(self.game.gadgets, robot)

        # update gadget to robot
        robot.gadgets[player_message.command] = gadget
