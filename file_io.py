import json
import os
import sys

import utils
from card import Card
from deck import Deck

CONFIG_LOCATION = os.path.join(os.path.expanduser('~'), '.config', 'spacepy')
CONFIG_FILE_NAME = 'spacepy.conf'

DEFAULT_DECK_LOCATION = os.path.join(os.path.expanduser('~'), '.spacepy')


def config_file_exist(file_path=None):
    if not file_path:
        file_path = os.path.join(CONFIG_LOCATION, CONFIG_FILE_NAME)
    return os.path.isfile(file_path)


def write_config(config_dict: dict, file_path=None):
    os.makedirs(CONFIG_LOCATION, exist_ok=True)
    if not file_path:
        file_path = os.path.join(CONFIG_LOCATION, CONFIG_FILE_NAME)
    with open(file_path, 'w') as f:
        json.dump(config_dict, f, indent=4)


def del_config(file_path=None):
    if not file_path:
        file_path = os.path.join(CONFIG_LOCATION, CONFIG_FILE_NAME)
    os.remove(file_path)


def read_config(file_path=None):
    if not file_path:
        file_path = os.path.join(CONFIG_LOCATION, CONFIG_FILE_NAME)

    with open(file_path, 'r') as f:
        dct = json.load(f)

    return dct


def write_deck(d: Deck, path=None):
    if not path:
        path = DEFAULT_DECK_LOCATION
    directory = os.path.join(path, d.title)
    os.makedirs(directory, exist_ok=True)
    for card in d:
        card_path = os.path.join(directory, str(card.my_uuid) + '.json')
        with open(card_path, 'w') as f:
            json.dump(card, f, default=utils.json_default,
                      indent=4)


def append_to_deck_from_stdin(d: Deck, save_deck=True, path=None):
    try:
        while True:
            description = ''
            while not description:
                description = input() if not sys.stdin.isatty() else \
                    input('[ctrl-c to quit] Card {} description > ')
            response = input() if not sys.stdin.isatty() else \
                input('[ctrl-c to quit] Card {} response    > ')
            c = Card(description, response)
            d.append(c)
    except (KeyboardInterrupt, EOFError):
        print('Done.')
    if save_deck:
        write_deck(d)


def read_deck(*, path=None, title):
    if not path:
        path = DEFAULT_DECK_LOCATION

    path = os.path.join(path, title)

    deck = Deck(title)
    with os.scandir(path) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file():
                with open(entry, 'r') as f:
                    card = json.load(f, object_hook=utils.json_object_hook)
                    deck.append(card)
    deck.sort(key=lambda c: c.time_created)
    return deck


def get_deck_names(path=None):
    if not path:
        path = DEFAULT_DECK_LOCATION
    names = []
    with os.scandir(path) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_dir():
                names.append(entry.name)
    return names
