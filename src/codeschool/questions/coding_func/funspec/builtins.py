def answer_key(func):
    """
    Decorating a function as the @answer_key, tells Funspec that this function
    should be used as the reference case when grading submissions.
    """

    func._is_answer_key = True
    return func
