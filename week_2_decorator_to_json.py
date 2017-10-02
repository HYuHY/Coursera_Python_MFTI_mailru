"""
декоратор to_json, который можно применить к различным функциям,
чтобы преобразовывать их возвращаемое значение в JSON-формат
"""

import json


def to_json(func):
    def wrapped(*args, **kwargs):
        data_out = func(*args, **kwargs)
        return json.dumps(data_out)
    return wrapped


@to_json
def func(a, b, c, **kwargs):
    """
    простая функция для демострации работы декоратора to_json
    """
    answer_1 = a**(b**c)
    answer_2 = kwargs
    return answer_1, answer_2


if __name__ == "__main__":
    print(func(4, 2, 3, d="обход блокировок", dl=("proxy", "VPN", "Tor", "i2p")))
