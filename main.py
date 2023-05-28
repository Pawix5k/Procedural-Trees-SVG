from trunk import Trunk, TreeParams, LeafParams, generate_tree
from svg import generate_svg_from_tree


root = Trunk()
tree_params_dict = {
    "depth_limit": 4,
    "no_growth_chance": 0.1,
    "delta_no_growth_chance": 0.15,
    "split_chance": 0.7,
    "delta_split_chance": 0.8,
    "angles_of_split": (-32., 32.),
    "offshoot_chance": 0.6,
    "delta_offshoot_chance": 0.8,
    "angles_of_offshoot": (-32., 32),
    "epsilon_angles": 0.4,
    "trunk_length": 120.,
    "delta_trunk_length": 0.87,
    "epsilon_trunk_length": 0.1,
    "initial_angle": 0.,
    "stop_no_growth_until": 3,
    "trunk_width": 50,
    "delta_trunk_width": 0.8,
}
tree_params = TreeParams(**tree_params_dict)

leaf_size = 40.0
leaf_angles = (-67.0, 67.0)
leaf_params = LeafParams(size=leaf_size, angles=leaf_angles)

print(leaf_params.size, "HERE")

generate_tree(root, tree_params)
generate_svg_from_tree(root, leaf_params)

# generate_svg_from_tree(root)
