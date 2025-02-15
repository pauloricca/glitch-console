import random
from glitch_console_types import Config, State
from utils import draw_into_frame, get_random_char

falling_characters = []


def print_falling_characters(state: State, config: Config):
    global falling_characters
                    
    # Update falling characters
    for i in range(len(falling_characters)):
        char, (x, y) = falling_characters[i]
        new_char = get_random_char()  # Use a wider range of characters
        falling_characters[i] = (new_char, (x + random.randint(-1, 1), y + 1))

    # Remove characters that have fallen off the screen
    falling_characters[:] = [fc for fc in falling_characters if fc[1][1] < state.height]

    # Occasionally add a new falling character
    if random.random() < config.falling_chars_new_prob:
        new_char = get_random_char()  # Use a wider range of characters
        new_x = random.randint(0, state.width - 1)
        falling_characters.append((new_char, (new_x, 0)))

    # Add falling characters to the frame with trails
    for char, (x, y) in falling_characters:
        if 0 <= y < state.height and 0 <= x < state.width:
            if (
                state.using_colour
                or random.random() < config.colour_probability
            ):
                formatted_char = f"\033[1;31m{char}\033[0m"
            else:
                formatted_char = char
            draw_into_frame(state.frame, formatted_char, x, y)

            # Add trails
            for i in range(1, 4):
                if y + i < state.height:
                    if (
                        state.using_colour
                        or random.random() < config.colour_probability
                    ):
                        trail_char = f"\033[1;31m{char}\033[0m"
                    else:
                        trail_char = get_random_char()
                    draw_into_frame(state.frame, trail_char, x, y + i)

