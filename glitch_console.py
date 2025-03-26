from copy import copy
from dataclasses import dataclass
import os
import random
import time
import sys

from glitch_console_types import Config, State
from log import log

from programmes.fake_error import print_fake_error
from programmes.game_of_life import print_game_of_life
from programmes.noisy_characters import print_noisy_characters
from programmes.scan import print_scan
from programmes.tetris import print_tetris
from programmes.connections import print_connections
from programmes.falling_characters import print_falling_characters
from programmes.glitch_characters import print_glitch_characters
from programmes.three_d_shapes import print_3d_shapes
from programmes.tv_glitch import print_tv_glitch
from programmes.water import print_water
from programmes.waves import print_waves
from programmes.strobe import print_strobe
from utils import draw_into_frame, get_empty_frame

START_STAGE = 6
FPS = 25
MIN_SLEEP_TIME = 0.01
DO_CLEAR_CONSOLE = False
DO_WRITE_OVER_PREVIOUS_FRAME = False
DO_PRINT_WITHOUT_NEW_LINES = True
DO_PRINT_STATS = True


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
        duration=10,
        tetris_new_prob=2,
        tetris_depth_movement=3,
        tetris_max_depth=500,
        tetris_start_moving_forward_prob = 0.02,
        tetris_start_moving_backwards_prob = 0.01,
        tetris_drop_prob = 0.01,
    ),
    Config(
        transition_time=10,
        duration=200,
        game_of_life_prob=1.0,
        waves_period=15,
        waves_amplitude=10,
        waves_speed=4,
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
    Config( # 5
        transition_time=15,
        duration=30,
        noisy_chars_period=5,
        noisy_chars_prob=0.1,
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
        tv_glitch_amplitude=100,
        tv_glitch_speed=30,
        tv_glitch_period=100,
    ),
    Config(
        transition_time=5,
        duration=10,
        noisy_chars_period=5,
        noisy_chars_prob=0.3,
        error_prob=0.2,
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
        noisy_chars_prob=0.5,
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
        falling_chars_new_prob=0.03,
        tetris_new_prob=0.05,
        water_period=6,
        water_amplitude=5,
        water_speed=3,
        scan_prob=1,
        scan_thickness=10,
        scan_speed=-100,
    ),
    Config(
        transition_time=15,
        duration=30,
        scan_prob=1,
        scan_thickness=20,
        scan_speed=-700,
        tv_glitch_amplitude=100,
        tv_glitch_speed=30,
        tv_glitch_period=100,
        tv_glitch_is_dual_axis=True,
        waves_period=5,
        waves_amplitude=15,
        waves_speed=4,
    ), # 9
    Config(
        transition_time=15,
        duration=30,
        noisy_chars_period=5,
        noisy_chars_prob=0.2,
        error_prob=0.1,
        glitch_chars_line_prob=0.02,
        glitch_chars_counter_prob=0.05,
        glitch_chars_command_prob=0.03,
        glitch_chars_question_prob=0.01,
        glitch_chars_char_prob=0.02,
        glitch_chars_prob_mutating_new_prob=0.01,
        glitch_chars_prob_mutating_existing_prob=0.001,
        three_d_shapes_prob=1.0,
        three_d_shapes_turning_off_prob=0.0,
        three_d_shapes_turning_on_prob=1.0,
        three_d_shapes_change_shape_prob=0.01,
        tv_glitch_amplitude=100,
        tv_glitch_speed=30,
        tv_glitch_period=100,
        tv_glitch_is_dual_axis=True,
    ),
    Config(
        transition_time=15,
        duration=30,
        scan_prob=1,
        scan_thickness=10,
        scan_speed=-50,
        game_of_life_prob=1.0,
    ),
    Config(
        transition_time=15,
        duration=30,
        noisy_chars_period=5,
        noisy_chars_prob=0.2,
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
last_frame_time = time.time()
has_finished_transition = False
number_of_lines_in_last_frame = 0
state: State = None

render_time_percentage = 0

def main():
    global current_config, state, number_of_lines_in_last_frame, current_config_index, previous_config, last_transition_time, has_finished_transition, FPS, DO_CLEAR_CONSOLE, DO_WRITE_OVER_PREVIOUS_FRAME, last_frame_time, render_time_percentage, MIN_SLEEP_TIME

    start_time = time.time()

    while True:
        current_time = time.time()
        time_since_last_frame = current_time - last_frame_time
        last_frame_time = current_time
        width = os.get_terminal_size().columns
        height = os.get_terminal_size().lines

        state = State(
            frame=get_empty_frame(width, height),
            time_since_start=current_time - start_time,
            time_since_last_frame=time_since_last_frame,
            width=width,
            height=height,
            is_blinking=not state.is_blinking if state else False,
            using_colour=state.using_colour if state else False,
            global_rotation=state.global_rotation if state else (0, 0, 0),
            global_rotation_is_rotating_fast=state.global_rotation_is_rotating_fast if state else False,
            global_rotation_time_since_last_speed_change=state.global_rotation_time_since_last_speed_change if state else 0,
        )

        # Global rotation
        if state.global_rotation_is_rotating_fast:
            if state.global_rotation_time_since_last_speed_change > current_config.global_rotation_speed_fast_time:
                state.global_rotation_is_rotating_fast = False
                state.global_rotation_time_since_last_speed_change = 0
        else:
            if state.global_rotation_time_since_last_speed_change > current_config.global_rotation_speed_slow_time:
                state.global_rotation_is_rotating_fast = True
                state.global_rotation_time_since_last_speed_change = 0
        
        state.global_rotation_time_since_last_speed_change += time_since_last_frame
        rotation_speed_multiplier = current_config.global_rotation_speed_fast_ratio if state.global_rotation_is_rotating_fast else 1

        state.global_rotation = (
            (state.global_rotation[0] + current_config.global_rotation_speed[0] * time_since_last_frame * rotation_speed_multiplier) % 360, 
            (state.global_rotation[1] + current_config.global_rotation_speed[1] * time_since_last_frame * rotation_speed_multiplier) % 360, 
            (state.global_rotation[2] + current_config.global_rotation_speed[2] * time_since_last_frame * rotation_speed_multiplier) % 360
        )

        # Colour
        if random.random() < (
            current_config.colours_turning_off_prob
            if state.using_colour
            else current_config.colours_turning_on_prob
        ):
            state.using_colour = not state.using_colour


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

        print_noisy_characters(state, current_config)
        print_3d_shapes(state, current_config)
        print_connections(state, current_config)
        print_tetris(state, current_config)
        print_falling_characters(state, current_config)
        print_glitch_characters(state, current_config)
        print_fake_error(state, current_config)
        print_scan(state, current_config)
        state.frame = [line[:state.width].ljust(state.width) for line in state.frame]
        print_game_of_life(state, current_config)

        # Pad the frame with spaces to make it the same width, and crop it to width
        # Useful if we see bugs but not always necessary
        # state.frame = [line[:state.width].ljust(state.width) for line in state.frame]


        print_waves(state, current_config)
        print_water(state, current_config)
        print_tv_glitch(state, current_config)
        print_strobe(state, current_config)

        # Clear the console
        if DO_CLEAR_CONSOLE:
            os.system("cls" if os.name == "nt" else "clear")

        if DO_WRITE_OVER_PREVIOUS_FRAME:
            # Empty the console's previous lines
            for _ in range(number_of_lines_in_last_frame):
                # print("\033[A\033[K", end="")
                print("\033[1A", end="\x1b[2K")

        if DO_PRINT_STATS:
            draw_into_frame(state.frame, f"Render time: {100 * render_time_percentage:.2f}%", 0, 0)
            draw_into_frame(state.frame, f"Time since start: {state.time_since_start:.1f}s", 0, 1)
            draw_into_frame(state.frame, f"Time since last transition: {(time.time() - last_transition_time):.1f}s", 0, 2)
            draw_into_frame(state.frame, f"Current stage index: {current_config_index}", 0, 3)

        # Render
        if DO_PRINT_WITHOUT_NEW_LINES:
            print(''.join(state.frame), end='', flush=True)
            # sys.stdout.write(''.join(state.frame))
            # sys.stdout.flush()
        else:
            print('\n'.join(state.frame))

        number_of_lines_in_last_frame = len(state.frame)

        render_time = time.time() - current_time
        render_time_percentage = render_time / (1 / FPS)

        time.sleep(max((1 / FPS) - render_time, MIN_SLEEP_TIME))


if __name__ == "__main__":
    main()
