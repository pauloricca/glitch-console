from dataclasses import dataclass
import math
import random
from glitch_console_types import Config
from utils import draw_into_frame, get_random_char, get_random_lower_case_char

X_SCALE = 1
Y_SCALE = 0.3
FULL_RADIUS = 20
VERTEX_DIAMETER = 1.5
DO_DRAW_SQUARE_VERTICES = False
PROB_NEW_VERTEX = 0.05
VERTEX_LIFE_TIME = 5
VERTEX_BLINKING_TIME = 2
PERCENTAGE_OF_EDGES = 0.5
MIN_NUMBER_OF_EDGES = 2
FOV = 256
VIEWER_DISTANCE = 100
EDGE_CHAR = "."
LABEL_DISTANCE = 10
LABEL_LENGTH = 5


@dataclass
class Vertex:
    position: tuple[float, float, float]
    label: str
    birth_time: int
    position_projected: tuple[int, int] = (0, 0)

@dataclass
class Edge:
    start: Vertex
    end: Vertex
    birth_time: int

vertices: list[Vertex] = []
edges: list[Edge] = []
is_drawing_connections = False




def rotate_point_3d(p: tuple[float, float, float], angle_x, angle_y, angle_z):
    x, y, z = p

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


def project_point_3d(p: tuple[float, float, float], width, height, fov, viewer_distance):
    x, y, z = p

    factor = fov / (viewer_distance + z)
    x = x * factor + width / 2
    y = -y * factor + height / 2
    return (int(x), int(y))


def draw_line(frame, p1: tuple[int, int], p2: tuple[int, int], config: Config):
    global EDGE_CHAR
    x1, y1 = p1
    x2, y2 = p2

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
                + (EDGE_CHAR if random.random() < config.connections_prob else " ")
                + frame[int(y)][int(x) + 1 :]
            )
        x += x_inc
        y += y_inc


def draw_vertex(frame, p: tuple[int, int], label, config: Config):
    x, y = p

    global VERTEX_DIAMETER, X_SCALE, Y_SCALE, LABEL_DISTANCE, LABEL_LENGTH
    radius = VERTEX_DIAMETER
    for i in range(int(-radius * 2), int(radius * 2 + 1)):
        for j in range(int(-radius * 2), int(radius * 2 + 1)):
            if (i ** 2) * X_SCALE + (j ** 2) * Y_SCALE <= radius ** 2:
                if 0 <= y + i < len(frame) and 0 <= x + j < len(frame[0]):
                    frame[y + i] = (
                        frame[y + i][: x + j]
                        + (get_random_char() if random.random() < config.connections_prob else " ")
                        + frame[y + i][x + j + 1 :]
                    )
    
    label_x = x - len(label) - LABEL_DISTANCE if x < len(frame[0]) / 2 else x + LABEL_DISTANCE
    label_y = y - 1
    label_with_border = [
        "─" * (LABEL_LENGTH + 4),
        "│ " + label + " │",
        "─" * (LABEL_LENGTH + 4),
    ]
    draw_into_frame(frame, label_with_border, label_x, label_y)



def print_connections(
    frame, elapsed_time, config: Config, is_blinking_on: bool
):
    global is_drawing_connections, vertices, edges, X_SCALE, Y_SCALE, PROB_NEW_VERTEX, VERTEX_LIFE_TIME, VERTEX_BLINKING_TIME, PERCENTAGE_OF_EDGES, MIN_NUMBER_OF_EDGES, FULL_RADIUS, FOV, VIEWER_DISTANCE, LABEL_LENGTH

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

    # Add new vertices and edges
    if random.random() < PROB_NEW_VERTEX:
        new_vertex = Vertex(
            position=(random.randint(-FULL_RADIUS, FULL_RADIUS), random.randint(-FULL_RADIUS, FULL_RADIUS), random.randint(-FULL_RADIUS, FULL_RADIUS)),
            label="".join([get_random_lower_case_char() for _ in range(LABEL_LENGTH)]),
            birth_time=elapsed_time,
        )
        vertices.append(new_vertex)

        for vertex in vertices:
            if random.random() < PERCENTAGE_OF_EDGES or len(edges) < MIN_NUMBER_OF_EDGES:
                new_edge = Edge(
                    start=vertex,
                    end=new_vertex,
                    birth_time=elapsed_time,
                )
                edges.append(new_edge)

    for vertex in vertices:
        if elapsed_time - vertex.birth_time > VERTEX_LIFE_TIME:
            vertices.remove(vertex)
            edges = [edge for edge in edges if edge.start != vertex and edge.end != vertex]
            continue

        rotated_vertex = rotate_point_3d(vertex.position, angle_x, angle_y, angle_z)
        scaled_vertex = (rotated_vertex[0] * X_SCALE, rotated_vertex[1] * Y_SCALE, rotated_vertex[2] * X_SCALE)
        vertex.position_projected = project_point_3d(
            scaled_vertex, width, height, fov=FOV, viewer_distance=VIEWER_DISTANCE
        )

        if elapsed_time - vertex.birth_time > VERTEX_BLINKING_TIME or is_blinking_on:
            draw_vertex(frame, vertex.position_projected, vertex.label, config)

    for edge in edges:
        draw_line(frame, edge.start.position_projected, edge.end.position_projected, config)

