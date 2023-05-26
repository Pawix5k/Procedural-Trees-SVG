import math

from trunk import Trunk


def get_end_cords(length: float, angle: int, start_x: int, start_y: int) -> tuple[int, int]:
    end_x = start_x + int(length * math.sin(math.radians(angle)))
    end_y = start_y - int(length * math.cos(math.radians(angle)))
    return end_x, end_y


def get_line_string(start_x: int, start_y: int, end_x: int, end_y: int, width: float):
    return f'<line x1="{start_x}" y1="{start_y}" x2="{end_x}" y2="{end_y}" stroke="black" stroke-width="{width}"/>'


def generate_lines(trunk: Trunk, start_x: int, start_y: int) -> None:
    lines = []
    def recursively_add_line(trunk: Trunk, start_x: int, start_y: int):
        end_x, end_y = get_end_cords(trunk.length, trunk.angle, start_x, start_y)
        lines.append([start_x, start_y, end_x, end_y, trunk.width])
        for child in trunk.children:
            recursively_add_line(child, end_x, end_y)

    recursively_add_line(trunk, start_x, start_y)
    return lines


def get_bounding_box(lines: list[int]) -> tuple[int]:
    x_min, y_min, x_max, y_max, _ = lines[0]
    for line in lines:
        for x_cord in line[::2]:
            x_min = min(x_min, x_cord)
            x_max = max(x_max, x_cord)
        for y_cord in line[1::2]:
            y_min = min(y_min, y_cord)
            y_max = max(y_max, y_cord)
    
    return x_min, y_min, x_max, y_max


def save_svg(svg_content: str) -> None:
    with open("my_tree.svg", "w") as file:
        file.write(svg_content)


def generate_svg_from_tree(trunk: Trunk) -> None:
    start_x = 0
    start_y = 0
    lines = generate_lines(trunk, start_x, start_y)
    bounding_box = get_bounding_box(lines)
    x_min, y_min, x_max, y_max = bounding_box
    vp = (
        x_min - 50,
        y_min - 50,
        x_max - x_min + 100,
        y_max - y_min + 100
    )
    svg_content = []
    svg_content.append(f'<svg viewBox="{vp[0]} {vp[1]} {vp[2]} {vp[3]}" xmlns="http://www.w3.org/2000/svg">')
    for line in lines:
        svg_content.append(get_line_string(*line))
    svg_content.append("</svg>")
    svg_content = "\n".join(svg_content)
    save_svg(svg_content)
