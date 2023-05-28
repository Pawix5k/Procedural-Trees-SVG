import math
import random
from collections import namedtuple

from trunk import Trunk, LeafParams

DrawableTrunk = namedtuple("DrawableTrunk", ["start_x", "start_y", "end_x", "end_y", "start_width", "end_width", "angle"])
DrawableLeaf = namedtuple("DrawableLeaf", ["start_x", "start_y", "size", "angle"])


def get_end_cords(length: float, angle: int, start_x: int, start_y: int) -> tuple[int, int]:
    end_x = start_x + int(length * math.sin(math.radians(angle)))
    end_y = start_y - int(length * math.cos(math.radians(angle)))
    return end_x, end_y


def get_trunk_svg_string(trunk: DrawableTrunk):
    a = get_end_cords(trunk.start_width / 2, trunk.angle - 90, trunk.start_x, trunk.start_y)
    b = get_end_cords(trunk.end_width / 2, trunk.angle - 90, trunk.end_x, trunk.end_y)
    c = get_end_cords(trunk.end_width / 2, trunk.angle, trunk.end_x, trunk.end_y)
    d = get_end_cords(trunk.end_width / 2, trunk.angle + 90, trunk.end_x, trunk.end_y)
    e = get_end_cords(trunk.start_width / 2, trunk.angle + 90, trunk.start_x, trunk.start_y)

    small_offset_left = get_end_cords(trunk.end_width / 4, trunk.angle - 90, 0, 0)
    small_offset_right = (-small_offset_left[0], -small_offset_left[1])
    small_offset_up = get_end_cords(trunk.end_width / 4, trunk.angle, 0, 0)

    bezier_a = (b[0] + small_offset_up[0], b[1] + small_offset_up[1])
    bezier_b = (c[0] + small_offset_left[0], c[1] + small_offset_left[1])
    bezier_c = (c[0] + small_offset_right[0], c[1] + small_offset_right[1])
    bezier_d = (d[0] + small_offset_up[0], d[1] + small_offset_up[1])

    return f'''
    <path d="M {a[0]} {a[1]} L {b[0]} {b[1]}
    C {bezier_a[0]} {bezier_a[1]}, {bezier_b[0]} {bezier_b[1]}, {c[0]} {c[1]}
    C {bezier_c[0]} {bezier_c[1]}, {bezier_d[0]} {bezier_d[1]}, {d[0]} {d[1]},
    L {e[0]} {e[1]}" stroke="black" stroke-width="3" fill="#6D3607"/>'''


def scale_points(points: list[tuple[float]], scale_factor):
    print(points[0][0])
    print(scale_factor)
    return [(p[0] * scale_factor, p[1] * scale_factor) for p in points]


def rotate_point(point, angle):
    x, y = point
    new_x = x * math.cos(math.radians(angle)) - y * math.sin(math.radians(angle))
    new_y = y * math.cos(math.radians(angle)) + x * math.sin(math.radians(angle))
    return new_x, new_y


def rotate_points(points: list[tuple[float]], angle):
    return [rotate_point(p, angle) for p in points]


def translate_points(points: list[tuple[float]], start_x, start_y):
    return [(p[0] + start_x, p[1] + start_y) for p in points]


def get_leaf_svg_string(leaf: DrawableLeaf, leaf_params: LeafParams):
    leaf_points = [point for point in leaf_params.points]
    leaf_points = scale_points(leaf_points, leaf.size)
    leaf_points = rotate_points(leaf_points, leaf.angle)
    leaf_points = translate_points(leaf_points, leaf.start_x, leaf.start_y)
    leaf_points = [f"{int(p[0])},{int(p[1])}" for p in leaf_points]

    return f'''
    <polygon points="{" ".join(leaf_points)}" stroke="black" stroke-width="3" fill="#0ecd17"/>
    '''


def get_shape_svg_string(shape: DrawableTrunk | DrawableLeaf, leaf_params: LeafParams) -> str:
    if type(shape) == DrawableTrunk:
        return get_trunk_svg_string(shape)
    if type(shape) == DrawableLeaf:
        return get_leaf_svg_string(shape, leaf_params)


def generate_shapes(trunk: Trunk, start_x: int, start_y: int, leaf_params: LeafParams) -> None:
    shapes = []
    def recursively_add_shape(trunk: Trunk, start_x: int, start_y: int):
        end_x, end_y = get_end_cords(trunk.length, trunk.angle, start_x, start_y)
        drawable_trunk = DrawableTrunk(start_x, start_y, end_x, end_y, trunk.start_width, trunk.end_width, trunk.angle)
        shapes.append(drawable_trunk)
        for leaf in trunk.leaves:
            left_offset = get_end_cords(drawable_trunk.end_width / 2, drawable_trunk.angle - 90, 0, 0)
            right_offset = (-left_offset[0], -left_offset[1])
            drawable_leaf = DrawableLeaf(
                leaf * (drawable_trunk.end_x - drawable_trunk.start_x) + start_x + left_offset[0],
                leaf * (drawable_trunk.end_y - drawable_trunk.start_y) + start_y + left_offset[1],
                leaf_params.size,
                leaf_params.angles[0] + drawable_trunk.angle + random.gauss() * 10.
            )
            shapes.append(drawable_leaf)
            drawable_leaf = DrawableLeaf(
                leaf * (drawable_trunk.end_x - drawable_trunk.start_x) + start_x + right_offset[0],
                leaf * (drawable_trunk.end_y - drawable_trunk.start_y) + start_y + right_offset[1],
                leaf_params.size,
                leaf_params.angles[1] + drawable_trunk.angle + random.gauss() * 10.
            )
            shapes.append(drawable_leaf)
        for child in trunk.children:
            recursively_add_shape(child, end_x, end_y)

    recursively_add_shape(trunk, start_x, start_y)
    return shapes


def get_bounding_box(drawable_trunks: list[DrawableTrunk]) -> tuple[int]:
    x_min = min(drawable_trunks[0].start_x, drawable_trunks[0].end_x)
    x_max = max(drawable_trunks[0].start_x, drawable_trunks[0].end_x)
    y_min = min(drawable_trunks[0].start_y, drawable_trunks[0].end_y)
    y_max = max(drawable_trunks[0].start_y, drawable_trunks[0].end_y)
    for line in drawable_trunks:
        for x_cord in (line.start_x, line.end_x):
            x_min = min(x_min, x_cord)
            x_max = max(x_max, x_cord)
        for y_cord in (line.start_y, line.end_y):
            y_min = min(y_min, y_cord)
            y_max = max(y_max, y_cord)
    
    return x_min, y_min, x_max, y_max


def save_svg(svg_content: str) -> None:
    with open("my_tree.svg", "w") as file:
        file.write(svg_content)


def generate_svg_from_tree(trunk: Trunk, leaf_params: LeafParams) -> None:
    start_x = 0
    start_y = 0
    shapes = generate_shapes(trunk, start_x, start_y, leaf_params)
    bounding_box = get_bounding_box([trunk for trunk in shapes if type(trunk) == DrawableTrunk])
    x_min, y_min, x_max, y_max = bounding_box
    vb = (
        x_min - 200,
        y_min - 200,
        x_max - x_min + 400,
        y_max - y_min + 400
    )

    svg_content = []
    svg_content.append(f'<svg viewBox="{vb[0]} {vb[1]} {vb[2]} {vb[3]}" xmlns="http://www.w3.org/2000/svg">')
    for shape in shapes:
        svg_content.append(get_shape_svg_string(shape, leaf_params))
    svg_content.append("</svg>")
    svg_content = "\n".join(svg_content)
    save_svg(svg_content)
