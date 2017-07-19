
def programming_language(language, raises=True):
    """
    Return the :cls:`codeschool.core.models.ProgrammingLanguage` object
    associated with the given language reference.

    If a ProgrammingLanguage object is passed, it is returned as is. This makes
    this function useful to normalize values that should be ProgrammingLanguage
    instances. If raises=False, it will return None for non-existing languages.

    Args:
        language:
            Either a ProgrammingLanguage object (which is returned as-is) or
            a string with the short reference to the language (e.g., 'python',
            'c', 'cpp', etc)
        raises:
            Controls if an exception should be raised if language does not exist
            (default is True).

    Returns:
        A :cls:`codeschool.core.models.ProgrammingLanguage` object.
    """

    from .models import ProgrammingLanguage

    if isinstance(language, ProgrammingLanguage):
        return language
    elif not raises and language is None:
        return None
    return ProgrammingLanguage.get_language(language, raises)
