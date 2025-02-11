import math
import random
from glitch_console_types import Config
from utils import get_random_char

X_SCALE = 0.5
Y_SCALE = 0.25
ATOM_RADIUS = 8


def rotate_point_3d(x, y, z, angle_x, angle_y, angle_z):
    # Rotate around x-axis
    cos_x, sin_x = math.cos(angle_x), math.sin(angle_x)
    y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x

    # Rotate around y-axis
    cos_y, sin_y = math.cos(angle_y), math.sin(angle_y)
    x, z = x * cos_y + z * sin_y, -x * sin_y + z * cos_y

    # Rotate around z-axis
    cos_z, sin_z = math.cos(angle_z), math.sin(angle_z)
    x, y = x * cos_z - y * sin_z, x * sin_z + y * cos_z

    return x, y, z


def project_point_3d(x, y, z, width, height, fov, viewer_distance):
    factor = fov / (viewer_distance + z)
    x = x * factor + width / 2
    y = -y * factor + height / 2
    return int(x), int(y)


def draw_molecule(frame, vertices, edges, width, height, angle_x, angle_y, angle_z, config: Config):
    global X_SCALE, Y_SCALE
    projected_vertices = []
    for vertex in vertices:
        rotated_vertex = rotate_point_3d(*vertex, angle_x, angle_y, angle_z)
        scaled_vertex = (rotated_vertex[0] * X_SCALE, rotated_vertex[1] * Y_SCALE, rotated_vertex[2] * X_SCALE)  # Scale down the shape
        projected_vertex = project_point_3d(
            *scaled_vertex, width, height, fov=256, viewer_distance=4
        )
        projected_vertices.append(projected_vertex)

    for edge in edges:
        start, end = edge
        x1, y1 = projected_vertices[start]
        x2, y2 = projected_vertices[end]
        draw_line(frame, x1, y1, x2, y2, config)

    for vertex in projected_vertices:
        x, y = vertex
        draw_circle(frame, x, y, config)


def draw_line(frame, x1, y1, x2, y2, config: Config):
    dx, dy = x2 - x1, y2 - y1
    steps = max(abs(dx), abs(dy))
    if steps == 0:
        x_inc, y_inc = 0, 0
    else:
        x_inc, y_inc = dx / steps, dy / steps
    x, y = x1, y1
    for _ in range(steps):
        if 0 <= int(y) < len(frame) and 0 <= int(x) < len(frame[0]):
            frame[int(y)] = (
                frame[int(y)][: int(x)]
                + (get_random_char() if random.random() < config.connections_prob else " ")
                + frame[int(y)][int(x) + 1 :]
            )
        x += x_inc
        y += y_inc


def draw_circle(frame, x, y, config: Config):
    global ATOM_RADIUS, X_SCALE, Y_SCALE
    radius = ATOM_RADIUS
    for i in range(int(-radius * Y_SCALE), int(radius * Y_SCALE + 1)):
        for j in range(int(-radius * X_SCALE), int(radius * X_SCALE + 1)):
            if i ** 2 + j ** 2 <= radius ** 2:
                if 0 <= y + i < len(frame) and 0 <= x + j < len(frame[0]):
                    frame[y + i] = (
                        frame[y + i][: x + j]
                        + (get_random_char() if random.random() < config.connections_prob else " ")
                        + frame[y + i][x + j + 1 :]
                    )


is_drawing_connections = False


def print_connections(
    frame, elapsed_time, config: Config
):
    global is_drawing_connections

    if config.connections_turning_on_prob == 0:
        is_drawing_connections = False
    elif random.random() < (
            config.connections_turning_off_prob
            if is_drawing_connections
            else config.connections_turning_on_prob
        ):
            is_drawing_connections = not is_drawing_connections

    if not is_drawing_connections:
        return

    width = len(frame[0])
    height = len(frame)
    angle_x = elapsed_time * 0.5
    angle_y = elapsed_time * 0.3
    angle_z = elapsed_time * 0.2

    # Define vertices and edges for a molecule
    molecule_vertices = [
        (0, 0, 0),
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
    ]
    molecule_edges = [
        (0, 1),
        (0, 2),
        (0, 3),
    ]

    draw_molecule(frame, molecule_vertices, molecule_edges, width, height, angle_x, angle_y, angle_z, config)
