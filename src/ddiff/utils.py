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


class FONT_STYLES:
    DEFAULT = "\033[39m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    INVISIBLE = "\033[08m"
    REVERCE = "\033[07m"
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    BG_DEFAULT = "\033[49m"
    RESET = "\033[0m"  #
