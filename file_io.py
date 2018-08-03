import json
import os

import utils
from deck import Deck


def write_deck(d: Deck, path):
    directory = os.path.join(path, d.title)
    os.makedirs(directory, exist_ok=True)
    for card in d:
        card_path = os.path.join(directory, str(card.my_uuid) + '.json')
        with open(card_path, 'w') as f:
            json.dump(card, f, default=utils.json_default,
                      indent=4)


def read_deck(path):
    title = os.path.basename(path)
    deck = Deck(title)
    with os.scandir(path) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file():
                with open(entry, 'r') as f:
                    card = json.load(f, object_hook=utils.json_object_hook)
                    deck.append(card)
    return deck
