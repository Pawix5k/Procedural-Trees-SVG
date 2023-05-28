from trunk import Trunk, TreeParams, LeafParams, Angle, generate_tree
from svg import generate_svg_from_tree


root = Trunk()
tree_params_dict = {
    "depth_limit": 4,
    "no_growth_chance": 0.1,
    "delta_no_growth_chance": 0.15,
    "split_chance": 0.7,
    "delta_split_chance": 0.8,
    "angles_of_split": (Angle(-25.), Angle(25.)),
    "offshoot_chance": 0.6,
    "delta_offshoot_chance": 0.8,
    "angles_of_offshoot": (Angle(-30.), Angle(30.)),
    "epsilon_angles": 0.0,
    "trunk_length": 120.,
    "delta_trunk_length": 0.87,
    "epsilon_trunk_length": 0.1,
    "initial_angle": 0.,
    "stop_no_growth_until": 3,
    "trunk_width": 50,
    "delta_trunk_width": 0.7,
}
tree_params = TreeParams(**tree_params_dict)

leaf_size = 20.0
leaf_angles = (-67.0, 67.0)
leaf_params = LeafParams(size=leaf_size, angles=leaf_angles)

print(leaf_params.size, "HERE")

generate_tree(root, tree_params)
generate_svg_from_tree(root, leaf_params)

# print(tree_params.gravity_factor)
# print("=== 330")
# print(tree_params.get_gravity_angle(Angle(330)).value)
# print("=== 30")
# print(tree_params.get_gravity_angle(Angle(30)).value)


# print("=== 210")
# print(tree_params.get_gravity_angle(Angle(210)).value)
# print("=== 150")
# print(tree_params.get_gravity_angle(Angle(150)).value)



