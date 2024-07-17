from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LANGUAGE_CHOICES = [(values[0] if values else label, label) for label, values, *_ in get_all_lexers()]
STYLE_CHOICES = [(value, value) for value in get_all_styles()]
