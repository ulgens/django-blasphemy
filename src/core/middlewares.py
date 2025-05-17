import json

import pygments
from debug_toolbar.middleware import get_show_toolbar as get_show_debug_toolbar
from django.http import HttpResponse
from pygments.formatters import HtmlFormatter
from pygments.lexers import JsonLexer

from core.utils import parse_bool


class NonHtmlDebugToolbarMiddleware:
    """
    The Django Debug Toolbar usually only works for views that return HTML.
    This middleware wraps any JSON response in HTML if the debug toolbar is
    enabled and show_debug_toolbar=true is in the query string.

    Adapted from: https://gist.github.com/fabiosussetto/c534d84cbbf7ab60b025#gistcomment-4581191
    Shared at: https://gist.github.com/ulgens/73fe671d54eff80edb54a30e255c6a5f
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # If the toolbar is not active, don't wrap the response.
        show_debug_toolbar = get_show_debug_toolbar(async_mode=False)
        if not show_debug_toolbar(request):
            return response

        # If "show_debug_toolbar=true" not in the query string, don't wrap the response.
        debug_param = request.GET.get("show_debug_toolbar")
        if not parse_bool(debug_param):
            return response

        # If the response is not JSON, don't wrap the response.
        if not response["Content-Type"].startswith("application/json"):
            return response

        # If the JSON response is coming from the debug toolbar itself, don't wrap the response.
        if b"/__debug__/" in response.content or b'class="djdt-color"' in response.content:
            return response

        # Build the highlighted JSON content
        content = json.dumps(
            json.loads(response.content),
            indent=2,
        )
        highlighted_content = pygments.highlight(
            code=content,
            lexer=JsonLexer(),
            formatter=HtmlFormatter(style="monokai", full=True),
        )

        # Build the response
        headers = response.headers.copy()
        headers["Content-Type"] = "text/html; charset=utf-8"

        html_response = HttpResponse(
            highlighted_content,
            status=response.status_code,
            headers=headers,
        )

        return html_response
