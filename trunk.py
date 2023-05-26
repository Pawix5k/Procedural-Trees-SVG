import random

from enum import Enum, auto
from itertools import accumulate


class Trunk:
    def __init__(self, angle: int = 0):
        self.angle = angle
        self.length = None
        self.width = None
        self.children = []

    def __repr__(self):
        return f"{self.__class__.__name__}(length={self.length}, angle={self.angle})"


class PartitionResults(Enum):
    SPLIT = auto()
    OFFSHOOT = auto()
    NO_GROWTH = auto()


class TreeParams:
    def __init__(
        self,
        depth_limit: int,
        no_growth_chance: float,
        delta_no_growth_chance: float,
        split_chance: float,
        delta_split_chance: float,
        angles_of_split: tuple[float],
        offshoot_chance: float,
        delta_offshoot_chance: float,
        angles_of_offshoot: tuple[float],
        epsilon_angles: float,
        trunk_length: float,
        delta_trunk_length: float,
        epsilon_trunk_length: float,
        initial_angle: float,
        stop_no_growth_until: int,
        trunk_width: float,
        delta_trunk_width: float,
    ):
        self.depth_limit = depth_limit
        self.no_growth_chance = no_growth_chance
        self.delta_no_growth_chance = delta_no_growth_chance
        self.split_chance = split_chance
        self.delta_split_chance = delta_split_chance
        self.angles_of_split = angles_of_split
        self.offshoot_chance = offshoot_chance
        self.delta_offshoot_chance = delta_offshoot_chance
        self.angles_of_offshoot = angles_of_offshoot
        self.epsilon_angles = epsilon_angles
        self.trunk_length = trunk_length
        self.delta_trunk_length = delta_trunk_length
        self.epsilon_trunk_length = epsilon_trunk_length
        self.inital_angle = initial_angle
        self.stop_no_growth_until = stop_no_growth_until
        self.trunk_width = trunk_width
        self.delta_trunk_width = delta_trunk_width
        self.cum_weights_of_partition = self.get_cum_weights_of_partition()
    
    def get_cum_weights_of_partition(self) -> list[float]:
        weights = [self.split_chance, self.offshoot_chance, self.no_growth_chance]
        cum_weights = list(accumulate(weights))
        return cum_weights

    def get_trunk_length(self) -> float:
        return self.trunk_length + random.gauss() * self.epsilon_trunk_length * self.trunk_length
    
    def get_partition_result(self, depth: int) -> PartitionResults:
        if depth < self.stop_no_growth_until:
            if random.random() * self.cum_weights_of_partition[1] < self.cum_weights_of_partition[0]:
                return PartitionResults.SPLIT
            return PartitionResults.OFFSHOOT
        random_in_interval = random.random() * self.cum_weights_of_partition[2]
        if random_in_interval < self.cum_weights_of_partition[0]:
            return PartitionResults.SPLIT
        elif random_in_interval < self.cum_weights_of_partition[1]:
            return PartitionResults.OFFSHOOT
        return PartitionResults.NO_GROWTH
    
    def get_left_split_angle(self) -> float:
        return self.angles_of_split[0] + random.gauss() * self.epsilon_angles * self.angles_of_split[0]

    def get_right_split_angle(self) -> float:
        return self.angles_of_split[1] + random.gauss() * self.epsilon_angles * self.angles_of_split[1]
    
    def get_offshoot_angle(self) -> float:
        angle = random.choice(self.angles_of_offshoot)
        return angle + random.gauss() * self.epsilon_angles * angle
    
    def update_all(self) -> None:
        self.no_growth_chance *= self.delta_no_growth_chance
        self.split_chance *= self.delta_split_chance
        self.offshoot_chance *= self.delta_offshoot_chance
        self.cum_weights_of_partition = self.get_cum_weights_of_partition()
        self.trunk_length *= self.delta_trunk_length
        self.trunk_width *= self.delta_trunk_width


def resolve_partition(trunk: Trunk, params: TreeParams, depth: int) -> None:
    if depth >= params.depth_limit:
        return
    result = params.get_partition_result(depth)
    print(result)
    if result == PartitionResults.SPLIT:
        trunk.children = [
            Trunk(trunk.angle + params.get_left_split_angle()),
            Trunk(trunk.angle + params.get_right_split_angle()),
        ]
    elif result == PartitionResults.OFFSHOOT:
        trunk.children = [
            Trunk(trunk.angle + params.get_offshoot_angle()),
        ]
    

def generate_tree(root: Trunk, params: TreeParams):
    # random.seed(341)
    depth = 0
    root.angle = params.inital_angle
    root.width = params.trunk_width
    children = [root]

    print(params.cum_weights_of_partition)

    while(children):
        new_children = []
        for child in children:
            child.length = params.get_trunk_length()
            child.width = params.trunk_width
            resolve_partition(child, params, depth)
            new_children.extend(child.children)
        depth += 1
        params.update_all()
        print(params.cum_weights_of_partition)
        children = new_children
