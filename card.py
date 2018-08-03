import time
import uuid
from typing import DefaultDict, Dict

import utils

ONE_DAY = 24 * 60 * 60


class Card:
    def __init__(self,
                 description: str,
                 response: str,
                 my_uuid: uuid.UUID = None,
                 easiness_factor: float = 2.5,
                 iteration_number: int = 0,
                 iteration_length: int = 0,
                 unix_time_to_review: float = None,
                 modification_times: Dict[str, float] = None):
        self.modification_times = DefaultDict(time.time)
        self.description = description
        self.response = response
        self.my_uuid = my_uuid if my_uuid else uuid.uuid4()
        self.easiness_factor = easiness_factor
        self.iteration_number = iteration_number
        self.iteration_length = iteration_length
        self.unix_time_to_review = unix_time_to_review \
            if unix_time_to_review \
            else time.time()
        if modification_times:
            if self._verify_dictionary(modification_times):
                self.modification_times.update(modification_times)
            else:
                raise KeyError

    def __setattr__(self, name, value):
        if name != 'modification_times':
            self.modification_times[name] = time.time()
        super().__setattr__(name, value)

    def _verify_dictionary(self, d: DefaultDict[str, float]):
        valid_keys = self.__dict__.keys()
        for key in d:
            if key not in valid_keys:
                return False
        return True

    @property
    def time_created(self):
        return self.modification_times['my_uuid']

    def rate_card(self, rating):
        self.easiness_factor = utils.calculate_easiness_delta(
            rating) + self.easiness_factor
        self.easiness_factor = max(self.easiness_factor, 1.3)

        self.iteration_number += 1
        if rating < 2:
            self.iteration_number = 0
            self.iteration_length = 0

        elif self.iteration_number == 1:
            self.iteration_length = ONE_DAY

        elif self.iteration_number == 2:
            self.iteration_length = 6 * ONE_DAY

        else:
            self.iteration_length = self.iteration_length \
                                    * self.easiness_factor

        self.unix_time_to_review = time.time() + self.iteration_length

    def is_reviewable(self, current_time=None):
        if current_time is None:
            current_time = time.time()
        return current_time >= self.unix_time_to_review

    def resolve(self, o):
        assert self.my_uuid == o.my_uuid
        return utils.recursive_dict_merge(self.__dict__, o.__dict__,
                                          lambda d, k: d['managed_dict'][k])

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __repr__(self):
        return 'Card({})'.format(', '.join(
            map(repr,
                [self.description,
                 self.response,
                 self.my_uuid,
                 self.easiness_factor,
                 self.iteration_number,
                 self.iteration_length,
                 self.unix_time_to_review,
                 self.modification_times
                 ])))
