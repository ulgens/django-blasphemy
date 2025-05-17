import socket

from django.conf import settings

__all__ = (
    "TRUE_VALUES",
    "parse_bool",
    "show_debug_toolbar",
)

TRUE_VALUES = ("t", "true", "1", 1, True)


def parse_bool(value):
    if isinstance(value, str):
        value = value.strip().lower()

    return value in TRUE_VALUES


def show_debug_toolbar(request):
    """
    Determine whether to show the toolbar on a given page.

    Adapted from debug_toolbar.middleware.show_toolbar,
    with the additional "Check url?show_debug_toolbar=true" block.
    """
    if not settings.DEBUG:
        return False

    # Check INTERNAL_IPS
    if request.META.get("REMOTE_ADDR") in settings.INTERNAL_IPS:
        return True

    # Check INTERNAL_IPS for Docker
    try:
        # This is a hack for docker installations. It attempts to look
        # up the IP address of the docker host.
        # This is not guaranteed to work.
        docker_ip = (
            # Convert the last segment of the IP address to be .1
            ".".join(socket.gethostbyname("host.docker.internal").rsplit(".")[:-1]) + ".1"
        )
        if request.META.get("REMOTE_ADDR") == docker_ip:
            return True
    except socket.gaierror:
        # It's fine if the lookup errored since they may not be using docker
        pass

    # Check url?show_debug_toolbar=true
    # The case this block solves could be handled by a better INTERNAL_IPS config,
    # but this is easier than handling the dynamic nature of things under remote K8S setups.
    debug_param = request.GET.get("show_debug_toolbar")
    if parse_bool(debug_param):  # noqa: SIM103
        return True

    # No test passed
    return False
