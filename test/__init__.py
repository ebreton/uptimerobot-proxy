import os
import json

from settings import TEST_PATH


def load_up():
    file_path = os.path.join(TEST_PATH, 'event_up.json')
    with open(file_path) as input:
        return json.load(input)


def load_down():
    file_path = os.path.join(TEST_PATH, 'event_down.json')
    with open(file_path) as input:
        return json.load(input)
