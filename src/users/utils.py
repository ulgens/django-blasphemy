from xkcdpass import xkcd_password

PASSWORD_WORDLIST = xkcd_password.generate_wordlist(min_length=6, max_length=15)


def generate_readable_password(acrostic: str = "") -> str:
    password = xkcd_password.generate_xkcdpassword(
        wordlist=PASSWORD_WORDLIST,
        acrostic=acrostic,
        case="random",
        delimiter="_",
    )

    return password
