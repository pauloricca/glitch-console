import time
from glitch_console_types import Config, State
import math

def print_tv_glitch(state: State, config: Config):
    if config.tv_glitch_amplitude == 0 or config.tv_glitch_period == 0:
        return

    t = time.time()

    offsets_y = [
        int(config.tv_glitch_amplitude * math.sin((y + config.tv_glitch_speed * t) / config.tv_glitch_period))
        for y in range(max(state.height, state.width))
    ]

    # Add horizontal shift on certain bands
    for band in range(0, state.height, 10):
        shift = int(config.tv_glitch_amplitude * math.sin((band + config.tv_glitch_speed * t) / config.tv_glitch_period))
        state.frame[band] = state.frame[band][shift:] + state.frame[band][:shift]

    state.frame = [
        "".join(
            state.frame
                [(y + (offsets_y[x if config.tv_glitch_is_swap_axis else y] if config.tv_glitch_is_dual_axis else 0)) % state.height]
                [(x + offsets_y[y if config.tv_glitch_is_swap_axis else x]) % state.width]
            for x in range(state.width)
        )
        for y in range(state.height)
    ]