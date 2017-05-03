from collections import Mapping

from ipware.ip import get_real_ip, get_ip as _get_ip


def get_ip(request):
    """
    Return the best possible inference for the user's ip address from a request.

    If ip cannot be determined, returns an empty string.
    """

    if not isinstance(request.META, Mapping):
        return ''
    return get_real_ip(request) or _get_ip(request) or ''
