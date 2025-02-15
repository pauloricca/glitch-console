from copy import copy
from dataclasses import dataclass
import os
import random
import time

from glitch_console_types import Config, State
from log import log

from programmes.fake_error import print_fake_error
from programmes.noisy_characters import print_noisy_characters
from programmes.tetris import print_tetris
from programmes.connections import print_connections
from programmes.falling_characters import print_falling_characters
from programmes.glitch_characters import print_glitch_characters
from programmes.three_d_shapes import print_3d_shapes
from programmes.water import print_water
from programmes.waves import print_waves

START_STAGE = 6
FPS = 30
DO_CLEAR_CONSOLE = False
DO_WRITE_OVER_PREVIOUS_FRAME = False
DO_PRINT_WITHOUT_NEW_LINES = True


stages: list[Config] = [
    Config(
        transition_time=3,
        duration=15,
        glitch_chars_print_at_bottom=True,
        glitch_chars_command_prob=0.02,
    ),
    Config(
        transition_time=8,
        duration=8,
        glitch_chars_print_at_bottom=True,
        glitch_chars_command_prob=0.01,
        glitch_chars_question_prob=0.005,
        # colours_turning_off_prob=0.5,
        # colours_turning_on_prob=0.005,
        glitch_chars_prob_mutating_new_prob=0.01,
        tetris_new_prob=0.03,
        tetris_move_sideways_prob = 0.1
    ),
    Config(
        transition_time=5,
        duration=10,
        tetris_new_prob=0.2,
        tetris_move_sideways_prob = 0.4,
        tetris_random_chars = True
    ),
    Config(
        transition_time=15,
        duration=20,
        tetris_new_prob=2,
        tetris_depth_movement=3,
        tetris_max_depth=500,
        tetris_start_moving_forward_prob = 0.02,
        tetris_start_moving_backwards_prob = 0.01,
        tetris_drop_prob = 0.01,
    ),
    Config(
        transition_time=10,
        duration=20,
        tetris_new_prob=5,
        tetris_depth_movement=1,
        tetris_max_depth=500,
        waves_period=5,
        waves_amplitude=15,
        waves_speed=4,
    ),
    Config(
        transition_time=15,
        duration=30,
        noisy_chars_period=5,
        noisy_chars_prob=1,
        error_prob=0.1,
        glitch_chars_line_prob=0.02,
        glitch_chars_counter_prob=0.05,
        glitch_chars_command_prob=0.03,
        glitch_chars_question_prob=0.01,
        glitch_chars_char_prob=0.02,
        glitch_chars_prob_mutating_new_prob=0.01,
        glitch_chars_prob_mutating_existing_prob=0.001,
        # colour_probability=0.1,
        # colours_turning_off_prob=0.1,
        # colours_turning_on_prob=0.01,
        three_d_shapes_prob=1.0,
        three_d_shapes_turning_off_prob=0.0,
        three_d_shapes_turning_on_prob=1.0,
        three_d_shapes_change_shape_prob=0.01,
        falling_chars_new_prob=0.03,
        tetris_new_prob=0.05,
        waves_period=5,
        waves_amplitude=10,
        waves_speed=2,
    ),
    Config(
        transition_time=15,
        duration=30,
        noisy_chars_period=5,
        noisy_chars_prob=1,
        error_prob=0.1,
        glitch_chars_line_prob=0.02,
        glitch_chars_counter_prob=0.05,
        glitch_chars_command_prob=0.03,
        glitch_chars_question_prob=0.01,
        glitch_chars_char_prob=0.02,
        glitch_chars_prob_mutating_new_prob=0.01,
        glitch_chars_prob_mutating_existing_prob=0.001,
        # colour_probability=0.1,
        # colours_turning_off_prob=0.1,
        # colours_turning_on_prob=0.01,
        connections_prob=1.0,
        connections_turning_off_prob=0.0,
        connections_turning_on_prob=1.0,
        connections_change_shape_prob=0.01,
    ),
    Config(
        transition_time=15,
        duration=30,
        noisy_chars_period=5,
        noisy_chars_prob=1,
        error_prob=0.1,
        glitch_chars_line_prob=0.02,
        glitch_chars_counter_prob=0.05,
        glitch_chars_command_prob=0.03,
        glitch_chars_question_prob=0.01,
        glitch_chars_char_prob=0.02,
        glitch_chars_prob_mutating_new_prob=0.01,
        glitch_chars_prob_mutating_existing_prob=0.001,
        # colour_probability=0.1,
        # colours_turning_off_prob=0.1,
        # colours_turning_on_prob=0.01,
        three_d_shapes_prob=1.0,
        three_d_shapes_turning_off_prob=0.0,
        three_d_shapes_turning_on_prob=1.0,
        three_d_shapes_change_shape_prob=0.01,
        falling_chars_new_prob=0.03,
        tetris_new_prob=0.05,
        water_period=1,
        water_amplitude=5,
        water_speed=6,
    ),
    Config(
        transition_time=15,
        duration=30,
        noisy_chars_period=5,
        noisy_chars_prob=1,
        error_prob=0.1,
        glitch_chars_line_prob=0.02,
        glitch_chars_counter_prob=0.05,
        glitch_chars_command_prob=0.03,
        glitch_chars_question_prob=0.01,
        glitch_chars_char_prob=0.02,
        glitch_chars_prob_mutating_new_prob=0.01,
        glitch_chars_prob_mutating_existing_prob=0.001,
        # colour_probability=0.1,
        # colours_turning_off_prob=0.1,
        # colours_turning_on_prob=0.01,
        three_d_shapes_prob=1.0,
        three_d_shapes_turning_off_prob=0.0,
        three_d_shapes_turning_on_prob=1.0,
        three_d_shapes_change_shape_prob=0.01,
    ),
]



current_config_index = START_STAGE
current_config = copy(stages[current_config_index])
previous_config = stages[current_config_index]
last_transition_time = time.time()
has_finished_transition = False
is_blinking_on = False
number_of_lines_in_last_frame = 0
state: State = None

def main():
    global current_config, is_blinking_on, number_of_lines_in_last_frame, current_config_index, previous_config, last_transition_time, has_finished_transition, FPS, DO_CLEAR_CONSOLE, DO_WRITE_OVER_PREVIOUS_FRAME

    start_time = time.time()

    while True:
        current_time = time.time()

        state = State(
            frame=[" " * os.get_terminal_size().columns for _ in range(os.get_terminal_size().lines)],
            time_since_start=current_time - start_time,
            time_since_last_frame=current_time - state.time_since_start if state else 0,
            width=os.get_terminal_size().columns,
            height=os.get_terminal_size().lines,
            is_blinking=state.is_blinking if state else False,
        )

        if current_time - last_transition_time >= current_config.duration:
            previous_config = stages[current_config_index]
            current_config_index = (current_config_index + 1) % len(stages)
            last_transition_time = current_time
            has_finished_transition = False

        if current_time - last_transition_time < current_config.transition_time:
            elapsed_transition_time = current_time - last_transition_time
            transition_progress = elapsed_transition_time / current_config.transition_time

            for attr in dir(current_config):
                if not attr.startswith("__") and not isinstance(getattr(current_config, attr), bool) and isinstance(getattr(current_config, attr), (int, float)):
                    target_value = getattr(stages[current_config_index], attr)
                    previous_value = getattr(previous_config, attr)
                    interpolated_value = previous_value + (target_value - previous_value) * transition_progress
                    setattr(current_config, attr, interpolated_value)
        elif not has_finished_transition:
            current_config = copy(stages[current_config_index])
            has_finished_transition = True

        if random.random() < (
            current_config.colours_turning_off_prob
            if current_config.using_colour
            else current_config.colours_turning_on_prob
        ):
            current_config.using_colour = not current_config.using_colour

        is_blinking_on = not is_blinking_on

        (width, height) = os.get_terminal_size()
        elapsed_time = current_time - start_time

        # Generate empty frame
        frame = [" " * width for _ in range(height)]

        print_noisy_characters(frame, elapsed_time, current_config)
        print_3d_shapes(frame, elapsed_time, current_config)
        print_connections(frame, elapsed_time, current_config, is_blinking_on)
        print_tetris(frame, current_config)
        print_falling_characters(frame, current_config)
        print_glitch_characters(frame, current_config, is_blinking_on)
        print_fake_error(frame, current_config, is_blinking_on)

        # Pad the frame with spaces to make it the same width, and crop it to width
        # frame = [line[:width].ljust(width) for line in frame]

        # limit the frame to the console's width
        frame = print_waves(frame, current_config)

        # limit the frame to the console's width
        frame = print_water(frame, current_config)

        # Clear the console
        if DO_CLEAR_CONSOLE:
            os.system("cls" if os.name == "nt" else "clear")

        if DO_WRITE_OVER_PREVIOUS_FRAME:
            # Empty the console's previous lines
            for _ in range(number_of_lines_in_last_frame):
                # print("\033[A\033[K", end="")
                print("\033[1A", end="\x1b[2K")

        # Render
        if DO_PRINT_WITHOUT_NEW_LINES:
            print(''.join(frame), end='', flush=True)
        else:
            print('\n'.join(frame))

        number_of_lines_in_last_frame = len(frame)

        time.sleep(1 / FPS)


if __name__ == "__main__":
    main()
