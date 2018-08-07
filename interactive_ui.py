import card
import file_io


def main():
    conf = get_config_if_exist()
    while True:
        main_menu()


def main_menu():
    result = prompt_menu(['Learn', 'New Deck', 'Edit Deck', 'Quit'])
    if result == 0:
        learn()
    elif result == 1:
        new_deck()
    elif result == 2:
        edit_deck()
    else:
        quit()


def learn():
    d = get_deck()
    active_cards = filter(lambda x: x.is_reviewable(), d)
    for card in active_cards:
        print(card.description)
        show = confirm('Show response? (No quits learning session)',
                       enter_is_yes=True)
        if not show:
            return
        print(card.response)
        result = prompt_menu(['Terrible', 'Tip of my tongue', 'Good', 'Easy'],
                             "How'd you do?")
        assert result in range(4)
        card.rate_card(result)
        print('\n' * 200, end='')
        file_io.write_deck(d)


def new_deck():
    print('Enter deck name.')
    name = input('> ')
    if not name:
        print('Cancelling.')


def get_deck():
    decks = file_io.get_deck_names()
    if not decks:
        return None
    result = prompt_menu(decks)
    return file_io.read_deck(title=decks[result])


def edit_deck():
    deck = get_deck()

    result = prompt_menu(['List cards', 'Edit card', 'Add cards'])
    if result == 0:
        for i, card in enumerate(deck):
            print('Description {}: {}'.format(i, card.description))
            print('Response    {}: {}'.format(i, card.response))
    if result == 1:
        pass
    if result == 2:
        add_cards(deck)


def add_cards(deck):
    while True:
        d = input('Card {} Description > '.format(len(deck)))
        if not d:
            print('Finished adding cards.')
        r = input('Card {} Response    > '.format(len(deck)))
        deck.append(card.Card(d, r))


def get_config_if_exist():
    if file_io.config_file_exist():
        config = file_io.read_config()
        return config


def prompt_menu(items, message='Select one of the following options.'):
    while True:
        print(message)
        for idx, item in enumerate(items):
            print('{}: {}'.format(idx, item))
        input_str = input('> ')
        try:
            num = int(input_str)
            if 0 <= num < len(items):
                return num
        except ValueError:
            pass
        print('Invalid input')


def prompt_with_default(message, default):
    print(message)
    result = input('[Default={}] > '.format(default))
    if not result:
        return default
    return result


def confirm(message, enter_is_yes=False):
    print(message)
    result = ''
    while not result or result[0] not in ['y', 'n']:
        result = input('Y/N: ').lower()
        if enter_is_yes and result == '':
            return True
    return True if result[0] == 'y' else False


if __name__ == '__main__':
    main()
