import time
from glitch_console_types import Config, State
import math


def print_waves(state: State, config: Config):
    if config.waves_amplitude == 0 or config.waves_period == 0:
        return

    t = time.time()
    offsets = [
        int(config.waves_amplitude * math.sin((x + config.waves_speed * t) / config.waves_period))
        for x in range(state.height if config.waves_is_warp_mode else state.width)
        ]

    state.frame = [
        "".join(
            state.frame[(y + offsets[y if config.waves_is_warp_mode else x]) % state.height][x]
            for x in range(state.width)
        )
        for y in range(state.height)
    ]
