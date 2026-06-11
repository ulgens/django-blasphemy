import json

import pygments
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.data import JsonLexer
from rest_framework.renderers import BaseRenderer, BrowsableAPIRenderer

__all__ = (
    "BrowsableHtmlRenderer",
    "JsonHtmlRenderer",
)


class BrowsableHtmlRenderer(BrowsableAPIRenderer):
    """
    Fixes format naming for DRF's own browsable interface.
    The original "api" wording is too broad and doesn't hint about the actual result.
    """

    format = "browsable-html"


class JsonHtmlRenderer(BaseRenderer):
    """
    Renders JSON in an HTML page,
    so Django Debug Toolbar can be rendered on top of it.
    """

    media_type = "text/html"
    format = "json-html"
    charset = "utf-8"

    indent = 4
    style = "monokai"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return pygments.highlight(
            code=json.dumps(data, indent=self.indent),
            lexer=JsonLexer(),
            formatter=HtmlFormatter(style=self.style, full=True),
        )
