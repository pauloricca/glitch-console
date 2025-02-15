from copy import copy
import random
from glitch_console_types import Config, State
from log import log
from utils import get_random_char
from dataclasses import dataclass



FRAMES_PER_MOVEMENT = 5
FALLING_SPEED = 3
FALLING_SPEED_BACKWARDS = -1
PERSPECTIVE = 500
PROBABILITY_TO_FOLLOW_DIRECTION_BIAS = 0.8
PROBABILITY_OF_ROTATION = 0.05



pieces4x4 = [
    [
        "  X ",
        "  X ",
        "  X ",
        "  X ",
    ],
    [
        " X  ",
        " X  ",
        " XX ",
        "    ",
    ],
    [
        "    ",
        " XX ",
        " XX ",
        "    ",
    ],
    [
        " X  ",
        " XX ",
        " X  ",
        "    ",
    ],
    [
        " X  ",
        " XX ",
        "  X ",
        "    ",
    ],
]

pieces2x2 = [
    [
        " X",
        " X",
    ],
    [
        "X ",
        "XX",
    ],
    [
        "XX",
        "XX",
    ],
    [
        "X ",
        "XX",
    ],
    [
        "X ",
        "XX",
    ],
]


@dataclass
class TetrisPiece:
    piece: list
    position: tuple[int, int, int]
    character: str
    direction_bias: int = 0
    scale: int = 1
    rotation: int = 0
    is_dropping: bool = False
    frames_since_last_movement: int = 0


tetris_pieces: list[TetrisPiece] = []
is_movingbackwards = False


def print_tetris(state: State, config: Config):
    global tetris_pieces, FRAMES_PER_MOVEMENT, FALLING_SPEED, FALLING_SPEED_BACKWARDS, PROBABILITY_TO_FOLLOW_DIRECTION_BIAS, PROBABILITY_OF_ROTATION, is_movingbackwards, pieces4x4

    if config.tetris_depth_movement == 0:
        is_movingbackwards = False
    elif random.random() < (config.tetris_start_moving_forward_prob if is_movingbackwards else config.tetris_start_moving_backwards_prob):
        is_movingbackwards = not is_movingbackwards

    # Update pieces
    for tetris_piece in tetris_pieces:
        if random.random() < PROBABILITY_OF_ROTATION and not is_movingbackwards:
            tetris_piece.rotation = (tetris_piece.rotation + random.randint(-1, 1)) % 4

        x, y, z = tetris_piece.position

        if random.random() < config.tetris_move_sideways_prob and not is_movingbackwards:
            if random.random() < PROBABILITY_TO_FOLLOW_DIRECTION_BIAS:
                x += tetris_piece.direction_bias
            else:
                x += random.choice([-1, 1])
        
        if random.random() < config.tetris_drop_prob:
            tetris_piece.is_dropping = True

        if tetris_piece.is_dropping:
            y += FALLING_SPEED if not is_movingbackwards else FALLING_SPEED_BACKWARDS
        else:
            tetris_piece.frames_since_last_movement += 1
            if tetris_piece.frames_since_last_movement == FRAMES_PER_MOVEMENT:
                y += 1 if not is_movingbackwards else 0
                tetris_piece.frames_since_last_movement = 0
        
        z -= config.tetris_depth_movement * (1 if not is_movingbackwards else -1)

        tetris_piece.position = (x, y, z)

    # Remove pieces that have reached the bottom of the screen
    tetris_pieces[:] = [fp for fp in tetris_pieces if fp.position[1] < state.height]

    # Occasionally add a new piece
    if not is_movingbackwards:
        for _ in range(max(int(config.tetris_new_prob), 1)):
            if random.random() < config.tetris_new_prob:
                tetris_pieces.append(
                    TetrisPiece(
                        piece=random.randint(0, len(pieces4x4) - 1),
                        position=(
                            random.randint(0, state.width - 1),
                            random.randint(0, state.height - 1),
                            random.randint(-int(config.tetris_max_depth), int(config.tetris_max_depth)) if config.tetris_max_depth > 1 else 0),
                        scale=random.choice(config.tetris_scale_prob_weights),
                        direction_bias=random.choice([-1, 1]),
                        character=get_random_char()
                    )
                )
                tetris_pieces.sort(key=lambda piece: -piece.position[2])


    # Draw pieces on the frame
    for tetris_piece in tetris_pieces:
        if 0 <= tetris_piece.position[1] < state.height and 0 <= tetris_piece.position[0] < state.width:
            draw_piece(state.frame, tetris_piece, state.using_colour, state.width, state.height, config)



def draw_piece(frame, tetris_piece: TetrisPiece, use_colors, width, height, config: Config):
    global PERSPECTIVE, pieces4x4, pieces2x2

    x = tetris_piece.position[0]
    y = tetris_piece.position[1]
    z = tetris_piece.position[2]

    if z <= -PERSPECTIVE: return

    # Calculate the vanishing point (centre of the screen)
    x_vp = width // 2
    y_vp = height // 2

    # Apply 3D projection
    scale = tetris_piece.scale * PERSPECTIVE / (PERSPECTIVE + z)
    x = int(x_vp + (x - x_vp) * scale)
    y = int(y_vp + (y - y_vp) * scale)

    # Exclude if off-screen
    if x < 0 - scale or x >= width + scale or y < 0 - scale or y >= height + scale:
        return
    
    # Rotate the piece
    if scale >= 1:
        piece = copy(pieces4x4[tetris_piece.piece])
    elif scale >= 0.95:
        piece = copy(pieces2x2[tetris_piece.piece])
    elif scale >= 0.85:
        piece = [["X"]]
    elif scale >= 0.65:
        piece = [["X"]]
        character = "."
    else:
        return

    scale = max(1, int(scale))

    if len(piece) > 1:
        for _ in range(tetris_piece.rotation):
            piece = rotate_piece(piece)

    character = get_random_char() if config.tetris_random_chars else tetris_piece.character

    character = "\033[1;31m" + character + "\033[0m" if use_colors else character

    # Draw the tetris piece on the frame
    for i in range(len(piece)):
        for j in range(len(piece[i])):
            if piece[i][j] == "X":
                for k in range(scale):
                    for l in range(scale):
                        if 0 <= y + i*scale + k < len(frame) and 0 <= x + j*scale + l < len(frame[0]):
                            frame[y + i*scale + k] = frame[y + i*scale + k][:x + j*scale + l] + character + frame[y + i*scale + k][x + j*scale + l + 1:]


def rotate_piece(piece):
    return list(map("".join, zip(*reversed(piece))))
