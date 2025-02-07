import math
import random

from mumbo_types import Config
from utils import get_random_char


def print_noisy_characters(frame, elapsed_time, current_config: Config):
	if current_config.noisy_chars_prob == 0:
		return

	width = len(frame[0])
	height = len(frame)

	empty_percentage = (
		(math.sin(2 * math.pi * elapsed_time / current_config.noisy_chars_period) ** 2 + 1) / 2
	) ** 0.01

	center_x, center_y = width // 2, height // 2

	for y in range(height):
		line = ""
		for x in range(width):
			distance_to_center = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
			probability = 1 / (1 + distance_to_center**2)
			if current_config.noisy_chars_prob * random.random() < empty_percentage * (1 - probability):
				line += frame[y][x]
			else:
				line += get_random_char()
		frame[y] = line