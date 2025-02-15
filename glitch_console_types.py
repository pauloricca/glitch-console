
from dataclasses import dataclass, field
from typing import List

def default_puzzle_piece_scale_probability_weights() -> List[float]:
    return [1]


@dataclass
class State:
    frame: list[str]
    time_since_start: float
    time_since_last_frame: float
    width: int
    height: int
    is_blinking: bool = False
    using_colour: bool = False
    global_rotation: tuple[float, float, float] = (0, 0, 0)
    global_rotation_is_rotating_fast: bool = False
    global_rotation_time_since_last_speed_change: float = 0


@dataclass
class Config:
    transition_time: float = 1 # time in seconds it takes to transition to this config
    duration: float = 0 # time in seconds to stay in this config
    colour_probability: float = 0
    colours_turning_off_prob: float = 0
    colours_turning_on_prob: float = 0
    noisy_chars_period: float = 5 # period of the sine function in seconds
    noisy_chars_prob: float = 0
    error_prob: float = 0
    glitch_chars_print_at_bottom: bool = False # When true, glitches appear like a normal console
    glitch_chars_line_prob: float = 0
    glitch_chars_counter_prob: float = 0
    glitch_chars_command_prob: float = 0
    glitch_chars_question_prob: float = 0
    glitch_chars_char_prob: float = 0
    glitch_chars_prob_mutating_new_prob: float = 0
    glitch_chars_prob_mutating_existing_prob: float = 0
    three_d_shapes_prob: float = 0
    three_d_shapes_change_shape_prob: float = 0
    three_d_shapes_turning_off_prob: float = 0
    three_d_shapes_turning_on_prob: float = 0
    connections_prob: float = 0
    connections_change_shape_prob: float = 0
    connections_turning_off_prob: float = 0
    connections_turning_on_prob: float = 0
    falling_chars_new_prob: float = 0
    tetris_new_prob: float = 0
    tetris_scale_prob_weights: List[float] = field(default_factory=default_puzzle_piece_scale_probability_weights)
    tetris_max_depth: float = 0
    tetris_depth_movement: float = 0
    tetris_start_moving_forward_prob: float = 0
    tetris_start_moving_backwards_prob: float = 0
    tetris_move_sideways_prob: float = 0
    tetris_drop_prob: float = 0
    tetris_random_chars: bool = False
    waves_period: float = 0
    waves_amplitude: float = 0
    waves_speed: float = 0
    water_period: float = 0
    water_amplitude: float = 0
    water_speed: float = 0
    global_rotation_speed = (0.05, 0.2, 0.05)
    global_rotation_speed_slow_time = 1.5
    global_rotation_speed_fast_time = 0.5
    global_rotation_speed_fast_ratio = 30




    
