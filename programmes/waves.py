import time
from glitch_console_types import Config
import math

IS_WARP_MODE = True


def print_waves(frame: list[str], config: Config):
    global IS_WARP_MODE

    if config.waves_amplitude == 0 or config.waves_period == 0:
        return frame

    width = len(frame[0])
    height = len(frame)

    t = time.time()
    offsets = [
        int(config.waves_amplitude * math.sin((x + config.waves_speed * t) / config.waves_period))
        for x in range(height if IS_WARP_MODE else width)
        ]

    new_frame = [
        "".join(
            frame[(y + offsets[y if IS_WARP_MODE else x]) % height][x]
            for x in range(width)
        )
        for y in range(height)
    ]
    
    return new_frame