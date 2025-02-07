from copy import copy
import random
from glitch_console_types import Config
from utils import get_random_char
from dataclasses import dataclass

@dataclass
class TetrisPiece:
    piece: list
    position: tuple[int, int, int]
    scale: int
    rotation: int = 0
    is_dropping: bool = False
    frames_since_last_movement: int = 0

tetris_pieces: list[TetrisPiece] = []

frames_per_movement = 5
probability_of_tetris_piece_rotating = 0.1
probability_of_tetris_piece_moving_sideways = 0.3
probability_of_tetris_piece_dropping = 0.01

def print_tetris(frame, config: Config):
    global tetris_pieces, frames_per_movement, probability_of_tetris_piece_rotating, probability_of_tetris_piece_dropping, probability_of_tetris_piece_moving_sideways

    width = len(frame[0])
    height = len(frame)

    # Update pieces
    for tetris_piece in tetris_pieces:
        if random.random() < probability_of_tetris_piece_rotating:
            tetris_piece.rotation = (tetris_piece.rotation + random.randint(-1, 1)) % 4

        x = tetris_piece.position[0]
        y = tetris_piece.position[1]
        z = tetris_piece.position[2]

        if random.random() < probability_of_tetris_piece_moving_sideways:
            x += random.choice([-1, 1]) * tetris_piece.scale
        
        if random.random() < probability_of_tetris_piece_dropping:
            tetris_piece.is_dropping = True

        if tetris_piece.is_dropping:
            y += 2 * tetris_piece.scale
        else:
            tetris_piece.frames_since_last_movement += 1
            if tetris_piece.frames_since_last_movement == frames_per_movement:
                y += 1 * tetris_piece.scale
                tetris_piece.frames_since_last_movement = 0
        
        tetris_piece.position = (x, y, z)

    # Remove pieces that have reached the bottom of the screen
    tetris_pieces[:] = [fp for fp in tetris_pieces if fp.position[1] < height]

    # Occasionally add a new piece
    if random.random() < config.tetris_new_prob:
        tetris_pieces.append(
            TetrisPiece(
                piece=get_random_piece(),
                position=(random.randint(0, width - 1), 0, random.randint(0, width - 1)),
                scale=random.choice(config.tetris_scale_prob_weights)
            )
        )


    # Draw pieces on the frame
    for tetris_piece in tetris_pieces:
        if 0 <= tetris_piece.position[1] < height and 0 <= tetris_piece.position[0] < width:
            draw_piece(frame, tetris_piece, config.using_colour, get_random_char())



def get_random_piece():
    pieces = [
        [
            "  X ",
            "  X ",
            "  X ",
            "  X "
        ],
        [
            " X  ",
            " X  ",
            " XX ",
            "    "
        ],
        [
            " X  ",
            " X  ",
            "  XX",
            "    "
        ],
        [
            "    ",
            " XX ",
            " XX ",
            "    "
        ],
        [
            " X  ",
            " XX ",
            " X  ",
            "    "
        ],
        [
            " X  ",
            " XX ",
            "  X ",
            "    "
        ],
        [
            "    ",
            "XXX ",
            " X  ",
            "    "
        ]
    ]
    return random.choice(pieces)


def draw_piece(frame, tetris_piece: TetrisPiece, use_colors, character):
    # Rotate the piece
    piece = copy(tetris_piece.piece)
    for _ in range(tetris_piece.rotation):
        piece = rotate_piece(piece)

    x = tetris_piece.position[0]
    y = tetris_piece.position[1]
    scale = tetris_piece.scale

    # Draw the tetris piece on the frame
    for i in range(len(piece)):
        for j in range(len(piece[i])):
            if piece[i][j] == "X":
                for k in range(scale):
                    for l in range(scale):
                        if 0 <= y + i*scale + k < len(frame) and 0 <= x + j*scale + l < len(frame[0]):
                            if use_colors:
                                frame[y + i*scale + k] = frame[y + i*scale + k][:x + j*scale + l] + "\033[1;31m" + character + "\033[0m" + frame[y + i*scale + k][x + j*scale + l + 1:]
                            else:
                                frame[y + i*scale + k] = frame[y + i*scale + k][:x + j*scale + l] + character + frame[y + i*scale + k][x + j*scale + l + 1:]


def rotate_piece(piece):
    return list(map("".join, zip(*reversed(piece))))
