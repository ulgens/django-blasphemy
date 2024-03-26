from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = get_all_lexers()
# TODO: Convert this to a choices class
LANGUAGE_CHOICES = []

for lexer in LEXERS:
    name = lexer[0]
    aliases = lexer[1]
    alias = aliases[0] if aliases else name.lower()

    LANGUAGE_CHOICES.append((name, alias))


STYLES = get_all_styles()
# TODO: Convert this to a choices class
STYLE_CHOICES = []

for style in STYLES:
    name = style
    alias = style.lower()

    STYLE_CHOICES.append((name, alias))
