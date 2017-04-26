import model_reference
from django.apps import apps
from faker import Factory

fake = Factory.create()
fake_br = Factory.create('pt-br')


def make_page(model, root='rogue-root', **kwargs):
    """
    Create a new saved page under RogueRoot.
    """

    if isinstance(model, str):
        model = apps.get_model(*model.split('.'))

    root = model_reference.load(root)
    page = model(**kwargs)
    page.full_clean(exclude=['depth', 'path'])
    root.add_child(instance=page)
    return page
