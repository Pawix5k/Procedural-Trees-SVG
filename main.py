from trunk import Trunk, TreeParams, generate_tree
from svg import generate_svg_from_tree


root = Trunk()
tree_params_dict = {
    "depth_limit": 7,
    "no_growth_chance": 0.1,
    "delta_no_growth_chance": 0.15,
    "split_chance": 0.7,
    "delta_split_chance": 0.8,
    "angles_of_split": (-15., 15.),
    "offshoot_chance": 0.6,
    "delta_offshoot_chance": 0.8,
    "angles_of_offshoot": (-15., 15.),
    "epsilon_angles": 0.4,
    "trunk_length": 300.,
    "delta_trunk_length": 0.87,
    "epsilon_trunk_length": 0.2,
    "initial_angle": 0.,
    "stop_no_growth_until": 3,
    "trunk_width": 50,
    "delta_trunk_width": 0.8,
}
tree_params = TreeParams(**tree_params_dict)

generate_tree(root, tree_params)
generate_svg_from_tree(root)
