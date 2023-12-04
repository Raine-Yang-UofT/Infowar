"""
Templates for prompts that ask users to select additional parameters
"""
from Framework import input_code


def select_direction(item, prompt: str):
    """
    Prompts that select a direction

    :param item: the item that needs additional parameters
    :param prompt: the prompt message
    :return: a copy of item object with updated parameters
    """
    command_input = input(f"{prompt}  {input_code.UP}: up  {input_code.DOWN}: down  {input_code.LEFT}: left  {input_code.RIGHT}: right")
    if command_input not in [input_code.UP, input_code.DOWN, input_code.LEFT, input_code.RIGHT]:
        raise input_code.InvalidCommandException()
    item.direction = input_code.get_direction_message(command_input)
    return item


def select_direction_and_range(item, direction_prompt: str, range_prompt: str):
    """
    Prompts that select a direction and a range

    :param item: the item that needs additional parameters
    :param direction_prompt: the prompt message for direction
    :param range_prompt: the prompt message for range
    :return: a copy of item object with updated parameters
    """
    command_input = input(f"{direction_prompt}  {input_code.UP}: up  {input_code.DOWN}: down  {input_code.LEFT}: left  {input_code.RIGHT}: right")
    range_input = input(f"{range_prompt} (range between {item.config.min_launch_range} - {item.config.max_launch_range})")
    if range_input.isdigit():
        range_input = int(range_input)
    else:
        raise input_code.InvalidCommandException()

    if ((command_input not in [input_code.UP, input_code.DOWN, input_code.LEFT, input_code.RIGHT])
            or range_input < item.config.min_launch_range or range_input > item.config.max_launch_range):
        raise input_code.InvalidCommandException()
    item.direction, item.range = input_code.get_direction_message(command_input), range_input  # update weapon message as firing direction and range
    return item
