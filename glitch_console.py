from copy import copy
import os
import random
import time

from glitch_console_types import Config
from log import log

from programmes.fake_error import print_fake_error
from programmes.noisy_characters import print_noisy_characters
from programmes.tetris import print_tetris
from programmes.three_d_shapes import print_3d_shapes
from programmes.falling_characters import print_falling_characters
from programmes.glitch_characters import print_glitch_characters
from programmes.waves import print_waves

START_STAGE = 2
FPS = 30

stages: list[Config] = [
    Config(
        transition_time=3,
        duration=15,
        glitch_chars_print_at_bottom=True,
        glitch_chars_command_prob=0.02,
    ),
    Config(
        transition_time=8,
        duration=15,
        glitch_chars_print_at_bottom=True,
        glitch_chars_command_prob=0.01,
        glitch_chars_question_prob=0.005,
        colours_turning_off_prob=0.5,
        colours_turning_on_prob=0.005,
        glitch_chars_prob_mutating_new_prob=0.01,
        tetris_new_prob=0.01,
    ),
    Config(
        transition_time=8,
        duration=15,
        glitch_chars_print_at_bottom=True,
        glitch_chars_command_prob=0.01,
        glitch_chars_question_prob=0.005,
        colours_turning_off_prob=0.5,
        colours_turning_on_prob=0.005,
        glitch_chars_prob_mutating_new_prob=0.01,
        tetris_new_prob=0.01,
        tetris_scale_prob_weights=[1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 5],
    ),
    Config(
        transition_time=15,
        duration=30,
        using_colour=False,
        noisy_chars_period=5,
        noisy_chars_prob=1,
        colour_probability=0.1,
        error_prob=0.1,
        glitch_chars_line_prob=0.02,
        glitch_chars_counter_prob=0.05,
        glitch_chars_command_prob=0.03,
        glitch_chars_question_prob=0.01,
        glitch_chars_char_prob=0.02,
        glitch_chars_prob_mutating_new_prob=0.01,
        glitch_chars_prob_mutating_existing_prob=0.001,
        colours_turning_off_prob=0.1,
        colours_turning_on_prob=0.01,
        three_d_shapes_prob=1.0,
        three_d_shapes_turning_off_prob=0.0,
        three_d_shapes_turning_on_prob=1.0,
        three_d_shapes_change_shape_prob=0.01,
        falling_chars_new_prob=0.03,
        tetris_new_prob=0.05,
        tetris_scale_prob_weights=[1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 5],
        waves_period=5,
        waves_amplitude=10,
        waves_speed=2,
    )
]



current_config_index = START_STAGE
current_config = copy(stages[current_config_index])
previous_config = stages[current_config_index]
last_transition_time = time.time()
has_finished_transition = False
is_blinking_on = False
number_of_lines_in_last_frame = 0


def main():
    global current_config, is_blinking_on, number_of_lines_in_last_frame, current_config_index, previous_config, last_transition_time, has_finished_transition, FPS

    start_time = time.time()

    while True:
        current_time = time.time()

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
            log("transtion complete")
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
        print_tetris(frame, current_config)
        print_falling_characters(frame, current_config)
        print_glitch_characters(frame, current_config)
        print_fake_error(frame, current_config, is_blinking_on)

        # limit the frame to the console's width
        frame = [line[:width] for line in frame]
        frame = print_waves(frame, current_config)

        # Clear the console
        # os.system("cls" if os.name == "nt" else "clear")

        # Empty the console's previous lines
        # for _ in range(number_of_lines_in_last_frame):
            ## print("\033[A\033[K", end="")
            # print("\033[1A", end="\x1b[2K")

        # Render
        for line in frame:
            print(line)

        number_of_lines_in_last_frame = len(frame)

        time.sleep(1 / FPS)


if __name__ == "__main__":
    main()
