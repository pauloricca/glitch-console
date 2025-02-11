import math
import random

from glitch_console_types import Config
from utils import draw_into_frame, get_random_char


def print_noisy_characters(frame, elapsed_time, config: Config):
	if config.noisy_chars_prob == 0:
		return

	width = len(frame[0])
	height = len(frame)

	empty_percentage = (
		(math.sin(2 * math.pi * elapsed_time / config.noisy_chars_period) ** 2 + 1) / 2
	) ** 0.01

	center_x, center_y = width // 2, height // 2

	for y in range(height):
		line = ""
		for x in range(width):
			distance_to_center = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
			probability = 1 / (1 + distance_to_center**2)
			if config.noisy_chars_prob * random.random() < empty_percentage * (1 - probability):
				line += frame[y][x]
			else:
				line += get_random_char()
		draw_into_frame(frame, line, 0, y)