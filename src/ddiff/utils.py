import random
import string
import uuid
from typing import Callable

from ddiff.configurations import Configurations


def random_phrase(n=32) -> str:
    if Configurations.debug:
        return "."
    phrase = "".join(random.choices(string.ascii_letters + string.digits, k=n))
    return phrase


def random_separator(n=32) -> str:
    if Configurations.debug:
        return "."
    _sep = random_phrase(n=n)
    return f"<{_sep}>"


def print_decorator() -> Callable:
    def _print_decorator(func) -> Callable:
        def wrapper(*args, **kwargs) -> Callable:
            if Configurations.debug:
                job_id = str(uuid.uuid4())[:6]
                print(f"START {job_id}\n\tfunc:\t{func.__name__}\n\targs:\t{args}\n\tkwargs:\t{kwargs}")
                res = func(*args, **kwargs)
                print(f"RETURN FROM {job_id}\n\treturn:\t{res}")
                return res
            else:
                res = func(*args, **kwargs)
                return res

        return wrapper

    return _print_decorator
