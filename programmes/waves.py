import time
from glitch_console_types import Config, State
import math

IS_WARP_MODE = True


def print_waves(state: State, config: Config):
    global IS_WARP_MODE

    if config.waves_amplitude == 0 or config.waves_period == 0:
        return

    t = time.time()
    offsets = [
        int(config.waves_amplitude * math.sin((x + config.waves_speed * t) / config.waves_period))
        for x in range(state.height if IS_WARP_MODE else state.width)
        ]

    state.frame = [
        "".join(
            state.frame[(y + offsets[y if IS_WARP_MODE else x]) % state.height][x]
            for x in range(state.width)
        )
        for y in range(state.height)
    ]
