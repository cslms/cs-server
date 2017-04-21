from codeschool.core.config_dict import ConfigDict, DataDict


def get_sys_page(name):
    """
    Return system page by named reference.
    """

    import model_reference
    return model_reference.load(name)


def get_wagtail_root():
    """
    Returns the Wagtail's root page.
    """

    return get_sys_page('root-page')


def get_programming_language(language, raises=True):
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

    from codeschool.core.models import ProgrammingLanguage

    if isinstance(language, ProgrammingLanguage):
        return language
    elif not raises and language is None:
        return None
    return ProgrammingLanguage.get_language(language, raises)


config_options = ConfigDict()
global_data_store = DataDict()
