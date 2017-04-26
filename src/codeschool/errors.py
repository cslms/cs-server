class InvalidSubmissionError(Exception):
    """
    Raised by compute_response() when the response is invalid.
    """


class GradingError(Exception):
    """
    Error raised during grading operations.
    """
