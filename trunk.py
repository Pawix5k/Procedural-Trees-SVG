import random

from enum import Enum, auto
from itertools import accumulate


class Angle:
    def __init__(self, value):
        self.value = self.normalize(value)
    
    def __add__(self, other):
        return Angle(self.value + other.value)

    def __radd__(self, other):
        return Angle(self.value + other.value)
    
    def __sub__(self, other):
        return Angle(self.value - other.value)

    def __rsub__(self, other):
        return Angle(self.value - other.value)
    
    def __mul__(self, other):
        return Angle(self.value * other)
    
    def __rmul__(self, other):
        return Angle(self.value * other)
    
    def normalize(self, value):
        return value % 360


class Trunk:
    def __init__(self, angle: int = 0):
        self.angle = angle
        self.length = None
        self.start_width = None
        self.end_width = None
        self.children = []
        self.leaves = []

    def __repr__(self):
        return f"{self.__class__.__name__}(length={self.length}, angle={self.angle})"


class LeafParams:
    def __init__(self, size: float, angles: tuple[float]):
        self.size = size
        self.angles = angles
        # self.points = [(0., 0.), (-0.5, -0.2), (-0.4, -0.35), (0., -1.), (0.4, -0.35), (0.5, -0.2)]
        self.points = [(0., 0.), (0., -0.3), (-0.5, -0.5), (-0.4, -0.65), (0., -1.3), (0.4, -0.65), (0.5, -0.5), (0., -0.3)]


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

        self.straightening_factor = 0.0
        # self.gravity_factor = 0.0
        self.gravity_factor = 0.2
    
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
    
    def get_gravity_angle(self, angle):
        if angle.value > 180:
            a1 = Angle(0) - angle
            a2 = angle - Angle(180)
            print(a1.value, a2.value)
            ang = a2

            if a1.value < a2.value:
                ang = a1
            if self.gravity_factor >= 0:
                return ang * self.gravity_factor
            return ang * self.gravity_factor
        else:
            a1 = angle
            a2 = Angle(180) - angle
            print(a1.value, a2.value)
            
            ang = a2
            if a1.value < a2.value:
                ang = a1
            if self.gravity_factor >= 0:
                return ang * -self.gravity_factor
            return ang * -self.gravity_factor
    
    def get_left_split_angle(self, parent_angle) -> float:
        parent_angle = Angle(parent_angle)
        comp_angle = parent_angle + self.angles_of_split[0] + random.gauss() * self.epsilon_angles * Angle(90) - parent_angle * self.straightening_factor
        print(f"pre grav {comp_angle.value}")
        comp_angle += self.get_gravity_angle(comp_angle)
        print(f"post grav {comp_angle.value}")
        return comp_angle.value

    def get_right_split_angle(self, parent_angle) -> float:
        parent_angle = Angle(parent_angle)
        comp_angle = parent_angle + self.angles_of_split[1] + random.gauss() * self.epsilon_angles * Angle(90) - parent_angle * self.straightening_factor
        print(f"pre grav {comp_angle.value}")
        comp_angle += self.get_gravity_angle(comp_angle)
        print(f"post grav {comp_angle.value}")
        return comp_angle.value
        
    def get_offshoot_angle(self, parent_angle) -> float:
        parent_angle = Angle(parent_angle)
        angle = random.choice(self.angles_of_offshoot)
        comp_angle = parent_angle + angle + random.gauss() * self.epsilon_angles * Angle(90) - parent_angle * self.straightening_factor
        print(f"pre grav {comp_angle.value}")
        comp_angle += self.get_gravity_angle(comp_angle)
        print(f"post grav {comp_angle.value}")
        return comp_angle.value
    
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
    if result == PartitionResults.SPLIT:
        trunk.children = [
            Trunk(params.get_left_split_angle(trunk.angle)),
            Trunk(params.get_right_split_angle(trunk.angle)),
        ]
    elif result == PartitionResults.OFFSHOOT:
        trunk.children = [
            Trunk(params.get_offshoot_angle(trunk.angle)),
            # Trunk(trunk.angle + random.gauss() * 10.0),
        ]
    

def generate_tree(root: Trunk, params: TreeParams):
    # random.seed(34145)
    depth = 0
    root.angle = params.inital_angle
    root.start_width = params.trunk_width
    root.end_width = params.trunk_width * params.delta_trunk_width
    children = [root]

    while(children):
        new_children = []
        for child in children:
            child.length = params.get_trunk_length()
            child.start_width = params.trunk_width
            child.end_width = params.trunk_width * params.delta_trunk_width
            resolve_partition(child, params, depth)
            if not child.children:
                child.leaves = [0.1, 0.5, 0.95]
            new_children.extend(child.children)
        depth += 1
        params.update_all()
        children = new_children
