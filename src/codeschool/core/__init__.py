from codeschool.core.config_dict import ConfigDict, DataDict


def sys_page(name):
    """
    Return system page by named reference.
    """

    import model_reference
    return model_reference.load(name)


def wagtail_root():
    """
    Returns the Wagtail's root page.
    """

    return sys_page('root-page')


def rogue_root():
    """
    Returns root for all rogue pages.
    """

    return sys_page('rogue-root')


def hidden_root():
    """
    Returns root for all rogue pages.
    """

    return sys_page('hidden-root')


config = ConfigDict()
data_store = DataDict()