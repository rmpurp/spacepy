import uuid
from typing import Union

import card


@DeprecationWarning
def uuid_to_unix_time(uuid1: uuid.UUID) -> float:
    return (uuid1.time - 0x01b21dd213814000) * 100 / 1e9


def calculate_easiness_delta(rating):
    return - 0.8 + 0.6 * rating - 0.1 * rating * rating


def fuzzy_match(itr, prefix: str):
    itr = list(itr)
    potential_matches = list(filter(lambda x: x.startswith(prefix), itr))

    return potential_matches


def json_default(o):
    if isinstance(o, card.Card):
        as_dict = dict(o.__dict__)
        as_dict['__class__'] = 'Card'
        return as_dict
    elif isinstance(o, uuid.UUID):
        return {'__class__': 'UUID', 'data': str(o)}

    raise TypeError


def json_object_hook(dct):
    if '__class__' in dct:
        if dct['__class__'] == 'Card':
            del dct['__class__']
            return card.Card(**dct)
        elif dct['__class__'] == 'UUID':
            return uuid.UUID(dct['data'])
    else:
        return dct


Number = Union[int, float]


def recursive_dict_merge(d1: dict, d2: dict, *args) -> dict:
    '''
    Recursively merge two dicts, returning a new dict.

    Recursive refers to the situation with a nested dict, where this function
    will be called on the two competing dictionaries and the merged version will
    be added to the final dictionary
    :param d1: the first dictionary
    :param d2: the second dictionary
    :param args: key functions for each layer called on dictionary values,
    with the left-most being the first, second for the next layer, etc.
    If not specified, is the identity function.
    :return: the merged dictionary
    '''

    if not args:
        key = lambda d, k: d[k]
    else:
        key = args[0]

    new_dict = dict()
    assert (d1.keys()) == d2.keys()
    for k in d1.keys():
        if isinstance(d1[k], dict):
            assert isinstance(d2[k], dict)
            d = recursive_dict_merge(d1[k],
                                     d2[k],
                                     *(args[1:] if len(args) > 1 else ()))
            new_dict[k] = d

        elif key(d1, k) > key(d2, k):
            new_dict[k] = d1[k]
        else:
            new_dict[k] = d2[k]
    return new_dict
