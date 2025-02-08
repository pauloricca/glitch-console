
from dataclasses import dataclass, field
from typing import List

def default_puzzle_piece_scale_probability_weights() -> List[float]:
    return [1]

@dataclass
class Config:
    transition_time: float = 1 # time in seconds it takes to transition to this config
    duration: float = 0 # time in seconds to stay in this config
    using_colour: bool = False
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
    falling_chars_new_prob: float = 0
    tetris_new_prob: float = 0
    tetris_scale_prob_weights: List[float] = field(default_factory=default_puzzle_piece_scale_probability_weights)
    tetris_max_depth: float = 0
    tetris_depth_movement: float = 0
    waves_period: float = 0
    waves_amplitude: float = 0
    waves_speed: float = 0




    
