import os
from datetime import datetime
from functools import wraps


def logger(path):

    def __logger(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            call_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            result = old_function(*args, **kwargs)
            with open(path, 'a', encoding='utf-8') as log_file:
                log_file.write(
                    f'{call_time} - {old_function.__name__} - '
                    f'args: {args}, kwargs: {kwargs} - '
                    f'return: {result}\n'
                )
            return result

        return new_function

    return __logger


class FlatIterator:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list
        self.outer = 0
        self.inner = 0

    def __iter__(self):
        return self

    def __next__(self):
        while self.outer < len(self.list_of_list):
            if self.inner < len(self.list_of_list[self.outer]):
                item = self.list_of_list[self.outer][self.inner]
                self.inner += 1
                return item
            self.outer += 1
            self.inner = 0
        raise StopIteration


@logger('iterator.log')
def test_1():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    return 'ok'


if __name__ == '__main__':
    log_path = 'iterator.log'
    if os.path.exists(log_path):
        os.remove(log_path)

    test_1()

    with open(log_path, encoding='utf-8') as log_file:
        print(log_file.read())