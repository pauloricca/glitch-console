import time
from glitch_console_types import Config
import math

X_Y_PERIOD_RATIO = 0.01

def print_water(frame: list[str], config: Config):
    global X_Y_PERIOD_RATIO

    if config.water_amplitude == 0 or config.water_period == 0:
        return frame

    width = len(frame[0])
    height = len(frame)

    t = time.time()
    # offsets_x = [
    #         int(config.water_amplitude * math.sin((x + config.water_speed * t) / config.water_period * X_Y_PERIOD_RATIO))
    #         for x in range(width)
    #     ]
    offsets_y = [
            int(config.water_amplitude * math.sin((y + config.water_speed * t) / config.water_period))
            for y in range(max(height, width))
        ]

    new_frame = [
        "".join(
            frame[y][(x + offsets_y[x]) % width]
            for x in range(width)
        )
        for y in range(height)
    ]
    
    return new_frame