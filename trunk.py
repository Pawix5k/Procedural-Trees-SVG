from enum import Enum, auto
import random

class Trunk:
    def __init__(self, length: float = 0, angle: int = 0):
        self.length = length
        self.angle = angle
        self.children = []
    
    def __repr__(self):
        return f"{self.__class__.__name__}(length={self.length}, angle={self.angle})"


class PartitionResults(Enum):
    SPLIT = auto()
    OFFSHOOT = auto()
    NO_GROWTH = auto()


DEPTH_LIMIT = 5

NO_GROWTH_CHANCE = 0.1
DELTA_NO_GROWTH_CHANCE = 1.5

SPLIT_CHANCE = 0.7
OFFSHOOT_CHANCE = 0.6
DELTA_SPLIT_OFFSHOOT_CHANCE = 0.95

ANGLES_OF_OFFSHOOT_SPLIT = (-15., 15.)

TRUNK_LENGTH = 10.
DELTA_TRUNK_LENGTH = 0.7


def get_partition_result(no_growth_chance, split_chance, offshoot_chance) -> PartitionResults:
    if random.random() < no_growth_chance:
        return PartitionResults.NO_GROWTH
    if random.random() < split_chance:
        return PartitionResults.SPLIT
    if random.random() < offshoot_chance:
        return PartitionResults.OFFSHOOT
    return PartitionResults.NO_GROWTH


def get_updated_chances(depth: int) -> tuple[float]:
    return (
        NO_GROWTH_CHANCE * DELTA_NO_GROWTH_CHANCE ** depth,
        SPLIT_CHANCE * DELTA_SPLIT_OFFSHOOT_CHANCE ** depth,
        OFFSHOOT_CHANCE * DELTA_SPLIT_OFFSHOOT_CHANCE ** depth,
    )


def get_updated_length(length: float):
    return length * DELTA_TRUNK_LENGTH


def generate_tree(trunk: Trunk, depth: int = 0):
    if depth >= DEPTH_LIMIT:
        return
    
    trunk_length = get_updated_length(trunk.length)
    result = get_partition_result(*get_updated_chances(depth))

    if result == PartitionResults.NO_GROWTH:
        return
    elif result == PartitionResults.SPLIT:
        left_d_angle, right_d_angle = ANGLES_OF_OFFSHOOT_SPLIT
        trunk.children.append(Trunk(trunk_length + random.gauss() * 0.2 * trunk_length, trunk.angle + (left_d_angle + random.gauss() * 0.4 * left_d_angle)))
        trunk.children.append(Trunk(trunk_length + random.gauss() * 0.2 * trunk_length, trunk.angle + (right_d_angle + random.gauss() * 0.4 * right_d_angle)))
    elif result == PartitionResults.OFFSHOOT:
        d_angle = random.choice(ANGLES_OF_OFFSHOOT_SPLIT)
        trunk.children.append(Trunk(trunk_length + random.gauss() * 0.2 * trunk_length, trunk.angle + (d_angle + random.gauss() * 0.4 * d_angle)))
    
    for child in trunk.children:
        generate_tree(child, depth + 1)
