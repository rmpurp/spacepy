import json
import os
import shutil
import sys

import utils
from card import Card
from deck import Deck

CONFIG_LOCATION = os.path.join(os.path.expanduser('~'), '.config', 'spacepy')
CONFIG_FILE_NAME = 'spacepy.conf'

DEFAULT_DECK_LOCATION = os.path.join(os.path.expanduser('~'), '.spacepy')


def config_file_exist(file_path=None):
    """
    Determine whether the config file exists given a directory.
    :param file_path: the location to check for the configuration file.
                      If None (default), checks ~/.config/spacepy/
    :return: true if file exists, false else
    """
    if not file_path:
        file_path = os.path.join(CONFIG_LOCATION, CONFIG_FILE_NAME)
    return os.path.isfile(file_path)


def write_config(config_dict: dict, file_path=None):
    """
    Writes the config to the given location.
    :param config_dict: dictionary of key-value pairs to save
    :param file_path: directory to write the configuration file to. If
                      None (default), writes to ~/.config/spacepy/
    """
    os.makedirs(CONFIG_LOCATION, exist_ok=True)
    if not file_path:
        file_path = os.path.join(CONFIG_LOCATION, CONFIG_FILE_NAME)
    with open(file_path, 'w') as f:
        json.dump(config_dict, f, indent=4)


def del_config(file_path=None):
    """
    Deletes the configuration file at the given location.
    :param file_path: the directory from which the configuration file will
                      deleted. If None (default), deletes from ~/.config/spacepy
    """
    if not file_path:
        file_path = os.path.join(CONFIG_LOCATION, CONFIG_FILE_NAME)
    os.remove(file_path)


def read_config(file_path=None):
    """
    Reads the configuration file at the given directory.
    :param file_path: the directory; if None (default), is ~/.config/spacepy
    :return: the configuration dictionary
    """
    if not file_path:
        file_path = os.path.join(CONFIG_LOCATION, CONFIG_FILE_NAME)

    with open(file_path, 'r') as f:
        dct = json.load(f)

    return dct


def write_deck(d: Deck, path=None):
    """
    Write the given deck to the given directory.
    :param d: the deck to write
    :param path: the directory to write the deck to. If None (default),
                 writes it to ~/.spacepy/<Deck title>. Note that the path
                 should not include the deck title, it will be added
                 automatically.
    """
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
    """
    Add cards to the deck given input from the standard input.

    Expects the description and response to be separated by a single new line;
    arbitrary new lines are allowed between cards.
    :param d: the deck to append to.
    :param save_deck: if true (default), writes the deck to the given path.
    :param path: the path to which the deck should be written.
                 If None (default), writes to ~/,spacepy/<Deck title>. Do not
                 add the deck directory to the path; it will be added
                 automatically.
    """
    try:
        while True:
            card_index = len(d)
            description = ''

            while not description:
                description = input() if not sys.stdin.isatty() else \
                    input('[ctrl-c to quit] Card {} description > '
                          .format(card_index))

            response = input() if not sys.stdin.isatty() else \
                input('[ctrl-c to quit] Card {} response    > '
                      .format(card_index))

            c = Card(description, response)
            d.append(c)

    except (KeyboardInterrupt, EOFError):
        print('Done.')
    if save_deck:
        write_deck(d)


def read_deck(*, path=None, title):
    """
    Read the deck at the given path to the deck directory.
    TODO: Finish me
    :param path:
    :param title:
    :return:
    """
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


def del_deck(*, path=None, title):
    if not path:
        path = DEFAULT_DECK_LOCATION

    path = os.path.join(path, title)
    shutil.rmtree(path)



def get_deck_names(path=None):
    if not path:
        path = DEFAULT_DECK_LOCATION
    names = []
    with os.scandir(path) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_dir():
                names.append(entry.name)
    return names
