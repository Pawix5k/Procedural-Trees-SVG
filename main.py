from trunk import Trunk, generate_tree
from svg import generate_svg_from_tree


root = Trunk(length=100.)

generate_tree(root, root.angle)

lines = generate_svg_from_tree(root, 0, 0)
# print(lines)
# for line in lines:
#     print(line)
