from typing import List, Iterable

import card


class Deck(List[card.Card]):

    def __init__(self, title: str, cards: Iterable[card.Card] = None):
        """
        A collection of cards.
        :param title: The name of the deck
        :param cards: optional iterable of cards to add to this Deck. If none
                      given, the deck will be initialized to be empty.
        """
        super().__init__()
        self.title = title
        if cards:
            self.extend(cards)

    def reviewable_cards(self):
        """
        Get the reviewable cards in self.
        :return: iterable of reviewable cards, sorted by most to least urgent.
        """
        return sorted(filter(lambda x: x.is_reviewable(), self),
                      key=lambda x: x.unix_time_to_review)


def create_test_deck():
    """
    Create a test deck with pre-made cards.
    :return: the test deck.
    """
    descriptions = ['the powerhouse of the cell',
                    'a delicious fruit',
                    'a disgusting pizza topping',
                    'Why']
    responses = ['mitochondria',
                 'banana',
                 'pineapple',
                 '為什麼']
    cards = [card.Card(d, r) for d, r in zip(descriptions, responses)]
    return Deck('TestDeck', cards)
