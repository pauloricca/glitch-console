import random
from glitch_console_types import Config, State
from utils import get_random_char
from log import log

PROBABILITY_OF_MESSING_UP = 0.2
RANDOMIZE_LIVING_PIECES_PROB = 0.5
RANDOMIZE_INTERVAL = 3
RANDOMIZE_THRESHOLD = 0.04
FORCE_RANDOMIZE_INTERVAL = 30

last_frame = None
last_time_randomized = 0


def print_game_of_life(state: State, config: Config):
    global last_frame, last_time_randomized

    if config.game_of_life_prob == 0:
        last_frame = None
        return
    
    frame = state.frame if last_frame is None else last_frame
    width = state.width
    height = state.height

    # Create a copy of the frame to store the next generation
    next_frame: list[str] = []

    # alive_pieces = ["█", "▓", "▒", "░", "▒", "▓", "█"]
    living_cells = 0

    # Iterate over each cell in the frame
    for i in range(height):
        line = ""
        for j in range(width):
            if random.random() > config.game_of_life_prob:
                line += state.frame[i][j] if random.random() > PROBABILITY_OF_MESSING_UP * config.game_of_life_prob else get_random_char()
                continue

            # Count the number of live neighbors
            live_neighbors = 0
            neighbour_character = ""
            for di in range(-1, 2):
                for dj in range(-1, 2):
                    if di == 0 and dj == 0:
                        continue
                    ni = i + di
                    nj = j + dj
                    if 0 <= ni < height and 0 <= nj < width and frame[ni][nj] != " ":
                        neighbour_character = frame[ni][nj]
                        live_neighbors += 1
            
            # Apply the rules of Conway's Game of Life
            if (frame[i][j] != " " and (live_neighbors < 2 or live_neighbors > 3)):
                line += " "
            elif live_neighbors == 3:
                living_cells += 1
                line += neighbour_character
            else:
                if frame[i][j] != " " :
                    living_cells += 1
                line += frame[i][j]

        next_frame.append(line)
    
    if config.game_of_life_prob <= 0.9:
        last_time_randomized = state.time_since_start

    if (((living_cells / (width * height)) < RANDOMIZE_THRESHOLD and state.time_since_start - last_time_randomized > RANDOMIZE_INTERVAL) or state.time_since_start - last_time_randomized > FORCE_RANDOMIZE_INTERVAL):
        last_time_randomized = state.time_since_start
        next_frame = ["".join([get_random_char() if random.random() < RANDOMIZE_LIVING_PIECES_PROB else " " for _ in range(width)]) for _ in range(height)]

    # Update the frame with the next generation
    state.frame = next_frame
    last_frame = next_frame
