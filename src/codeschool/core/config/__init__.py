from .config_dict import ConfigDict, DataDict


def get_sys_page(name):
    """
    Return system page by named reference.
    """

    import model_reference
    return model_reference.load(name)


def wagtail_root():
    """
    Returns the Wagtail's root page.
    """

    return get_sys_page('root-page')


config_options = ConfigDict()
global_data_store = DataDict()
