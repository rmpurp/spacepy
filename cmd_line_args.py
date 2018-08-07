import argparse

import file_io
from deck import Deck
from utils import fuzzy_match


def new_deck(args):
    name = args.name
    __new_deck(name)


def __new_deck(name):
    if name in file_io.get_deck_names():
        print('Error: name already exists')
        exit(1)
    else:
        d = Deck(name)
        file_io.write_deck(d)


def append(args):
    name = args.deck
    if args.create:
        __new_deck(name)
    else:
        name = deck_match(name)
    deck = file_io.read_deck(title=name)
    file_io.append_to_deck_from_stdin(deck)


def deck_match(given_name, exit_if_none=True, exit_if_more_than_one=True):
    matches = list(fuzzy_match(file_io.get_deck_names(), given_name))
    if given_name in matches:
        return given_name
    if exit_if_none and not matches:
        print('No deck matches {}'.format(given_name))
        exit(1)
    elif exit_if_more_than_one and len(matches) > 1:
        print('Ambiguous: {} could be {}'.format(given_name, matches))
        exit(1)
    else:
        return matches[0]


def view(args):
    if not args.deck:
        for deck_name in file_io.get_deck_names():
            print(deck_name)
    else:
        deck_name = deck_match(args.deck)
        deck_name = file_io.read_deck(title=deck_name)
        for card in deck_name:
            print(card.description, card.response, sep='\n', end='\n\n')


def learn(args):
    pass


def edit(args):
    pass


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    new_parser = subparsers.add_parser('new',
                                       help='Create a new deck')
    new_parser.add_argument('name', metavar='N',
                            help='name of deck to create')
    new_parser.set_defaults(func=new_deck)
    learn_parser = subparsers.add_parser('learn',
                                         help='Learn deck')
    learn_parser.add_argument('deck', metavar='D',
                              help='name of deck to learn')
    learn_parser.add_argument('number', metavar='N',
                              default=99999, help='Number of cards to learn')
    learn_parser.set_defaults(func=learn)
    append_parser = subparsers.add_parser('append',
                                          help='Append from stdin to deck.')
    append_parser.add_argument('deck', metavar='D',
                               help='name of deck to append to')
    append_parser.add_argument('-c', '--create', action='store_true',
                               help='If flag is set, create the deck. Errors if'
                                    'deck already exists.')
    append_parser.set_defaults(func=append)
    view_parser = subparsers.add_parser('view', help='View decks or cards.')
    view_parser.add_argument('deck', metavar='D', help='', nargs='?',
                             default=None)
    view_parser.set_defaults(func=view)
    edit_parser = subparsers.add_parser('edit', help='Edit or delete a card in'
                                                     'a deck.')
    edit_parser.add_argument('deck', metavar='D', nargs=1, help='The deck')
    edit_parser.add_argument('card_num', metavar='N', nargs=1,
                             help='The index of the card to edit')
    edit_parser.add_argument('-d', '--delete', action='store_true',
                             help='If set, deletes the associated card. Else,'
                                  'prompts to edit it.')
    edit_parser.set_defaults(func=edit)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
