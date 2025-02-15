import random
import shutil


def get_terminal_size():
    return shutil.get_terminal_size((80, 20))


def get_random_char():
    return chr(random.randint(33, 126))

def get_random_lower_case_char():
    return chr(random.randint(97, 122))

def get_empty_frame(width, height):
    return [" " * width for _ in range(height)]

# Mutate error message characters
def mutate(string_or_string_list, probability):
    is_list = isinstance(string_or_string_list, list)

    string_list = string_or_string_list if is_list else [string_or_string_list]
    new_string_list = [None] * len(string_list)

    for i in range(len(string_list)):
        new_string_list[i] = "".join(
            (get_random_char() if random.random() < probability else char) for char in string_list[i]
        )

    if is_list:
        return new_string_list
    else:
        return new_string_list[0]


from typing import List, Union

def draw_into_frame(frame: List[str], content: Union[str, List[str]], x: int, y: int):
    if isinstance(content, str):
        content = [content]

    for i, line in enumerate(content):
        if 0 <= y + i < len(frame):
            if x < 0:
                line = line[-x:]
                x = 0
            if x + len(line) > len(frame[y + i]):
                line = line[:len(frame[y + i]) - x]
            frame[y + i] = frame[y + i][:x] + line + frame[y + i][x + len(line):]
    