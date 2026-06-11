from rest_framework.renderers import BrowsableAPIRenderer

__all__ = ("BrowsableHtmlRenderer",)


class BrowsableHtmlRenderer(BrowsableAPIRenderer):
    """
    Fixes format naming for DRF's own browsable interface.
    The original "api" wording is too broad and doesn't hint about the actual result.
    """

    format = "browsable-html"
