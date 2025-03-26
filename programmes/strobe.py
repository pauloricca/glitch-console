import random
from glitch_console_types import Config, State

is_strobing = False
is_strobing_inverted = False
PROBABILITY_OF_INVERTING_STROBE_MID_FRAME = 0.0001

def print_strobe(state: State, config: Config):
    global is_strobing

    if config.strobe_prob == 0:
        return

    if random.random() > config.strobe_prob:
        if is_strobing:
            is_strobing = False
    elif not is_strobing:
        is_strobing = True
    
    if not is_strobing:
        return

    def get_character(is_on: bool):
        global is_strobing_inverted

        if random.random() < PROBABILITY_OF_INVERTING_STROBE_MID_FRAME: 
            is_strobing_inverted = not is_strobing_inverted

        if is_on ^ is_strobing_inverted:
            return chr(9608) if state.is_blinking else " "
        else:
            return chr(9608) if not state.is_blinking else " "


    state.frame = [
        "".join(
            [get_character(True) if c != " " else get_character(False) for c in state.frame[y]]
        )
        for y in range(state.height)
    ]
