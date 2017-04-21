from ipware.ip import get_real_ip, get_ip as _get_ip


def get_ip(request):
    """
    Return the best possible inference for the user's ip address from a request.
    """

    return get_real_ip(request) or _get_ip(request) or ''