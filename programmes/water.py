import time
from glitch_console_types import Config, State
import math

X_Y_PERIOD_RATIO = 0.01

def print_water(state: State, config: Config):
    global X_Y_PERIOD_RATIO

    if config.water_amplitude == 0 or config.water_period == 0:
        return

    t = time.time()
    # offsets_x = [
    #         int(config.water_amplitude * math.sin((x + config.water_speed * t) / config.water_period * X_Y_PERIOD_RATIO))
    #         for x in range(width)
    #     ]
    offsets_y = [
            int(config.water_amplitude * math.sin((y + config.water_speed * t) / config.water_period))
            for y in range(max(state.height, state.width))
        ]
    
    state.frame = [
        "".join(
            state.frame[y][(x + offsets_y[x]) % state.width]
            for x in range(state.width)
        )
        for y in range(state.height)
    ]