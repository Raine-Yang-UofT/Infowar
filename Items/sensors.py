"""
Sensor items
"""

from dataclasses import dataclass


@dataclass
class SoundSensor:
    """
    Detect sound signal at a square region with a given radius around player
    Emits heat signal

    Representation invariants:
        -radius: the detection radius
        -heat_emission: the heat emitted
    """
    radius: int
    heat_emission: int


@dataclass
class HeatSensor:
    """
    Detect heat signal at a square region with a given radius around player
    Emits sound signal

    Representation invariants:
        -radius: the detection radius
        -sound_emission: the sound emitted
    """
    radius: int
    sound_emission: int
