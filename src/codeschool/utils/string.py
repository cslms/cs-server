import hashlib
from functools import lru_cache


def indent(text, prefix=4):
    """
    Indent string of text.
    """

    if isinstance(prefix, int):
        prefix = ' ' * prefix
    return '\n'.join(prefix + line for line in text.splitlines())


@lru_cache(1024)
def md5hash(st):
    """
    Compute the hex-md5 hash of string.

    Returns a string of 32 ascii characters.
    """

    return hashlib.md5(st.encode('utf8')).hexdigest()


def md5hash_seq(seq):
    """
    Combined md5hash for a sequence of string parameters.
    """

    hashes = [md5hash(x) for x in seq]
    return md5hash(''.join(hashes))