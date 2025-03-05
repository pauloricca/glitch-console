import random
from glitch_console_types import Config, State
from utils import draw_into_frame

bar_y_pos: float = 0
MARGIN_ABOVE_AND_BELOW_SCREEN = 0.5

def print_scan(state: State, config: Config):
    global bar_y_pos, MARGIN_ABOVE_AND_BELOW_SCREEN

    bar_y_pos += float(state.time_since_last_frame) * config.scan_speed

    # Wrap the bar around the screen
    if (bar_y_pos >= state.height * (1 + MARGIN_ABOVE_AND_BELOW_SCREEN)):
        bar_y_pos = -state.height * MARGIN_ABOVE_AND_BELOW_SCREEN
    elif (bar_y_pos < -state.height * MARGIN_ABOVE_AND_BELOW_SCREEN):
        bar_y_pos = state.height * (1 + MARGIN_ABOVE_AND_BELOW_SCREEN)

    if config.scan_prob == 0 or not state.is_blinking:
        return

    # Draw the horizontal bar
    lines: list[str] = []
    for _ in range(int(config.scan_thickness)):
        line = "".join(["█" if random.random() < config.scan_prob else " " for _ in range(state.width)])
        lines.append(line)

    draw_into_frame(state.frame, lines, 0, int(bar_y_pos))
