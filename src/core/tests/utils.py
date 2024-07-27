import random


def alternating_case(text):
    return "".join([char.upper() if i % 2 == 0 else char.lower() for i, char in enumerate(text)])


def random_case(text):
    case_func = random.choice([lambda t: t.lower(), lambda t: t.upper()])  # noqa: S311
    return "".join([case_func(char) for char in text])


# Inspired from xkcdpass.xkcd_password.CASE_METHODS
CASE_FUNCTIONS = {
    "as-is": lambda text: text,
    "lower": lambda text: text.lower(),
    "upper": lambda text: text.upper(),
    "title": lambda text: text.title(),
    "alternating": alternating_case,
    "random": random_case,
}
