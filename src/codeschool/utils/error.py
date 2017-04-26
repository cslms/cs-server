#
# Error handling utilities
#


def exception_to_json(ex):
    """
    JSON compatible representation of an exception.
    """

    return {
        'exception': ex.__class__.__name__,
        'message': ex.args,
    }
