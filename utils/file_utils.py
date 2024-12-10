# utils/file_utils.py
import json
import random
from colorama import Fore


def read_json(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"File '{filename}' not found")
        return None
    except json.JSONDecodeError:
        print(f"File '{filename}' is not a valid JSON")
        return None


def get_random_color():
    colors = [Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW,
              Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
    return random.choice(colors)
