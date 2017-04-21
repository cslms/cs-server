import random
from codeschool.factories import fake

star_wars_characters = [
    'han solo', 'darth vader', 'c3po', 'r2d2', 'luke skywalker',
    'princess leia', 'jabba', 'obi wan', 'yoda', 'jar jar binks',
]
adjective_list = [
    'grumpy', 'heroic', 'coward', 'brave', 'treacherous', 'powerful',
    'influential',
]
phrase_groups = []


def is_phase_provider(func):
    phrase_groups.append(func)
    return func


def phrase(maker=None):
    """
    A random easy to memorize phrase.
    """

    maker = random.choice(phrase_groups)
    return maker()


@is_phase_provider
def random_star_wars_phrase():
    """
    Random phrase based on Star Wars ;-)
    """

    subjective = random.choice(star_wars_characters)
    adjective = random.choice(adjective_list)
    return '%s %s' % (adjective, subjective)


@is_phase_provider
def random_fake_phrase():
    """
    Use fake-factory names.
    """

    adjective = random.choice(adjective_list)
    return '%s %s' % (fake.first_name(), adjective)


@is_phase_provider
def random_fake_catch():
    """
    Catch phrases
    """

    return fake.catch_phrase()
