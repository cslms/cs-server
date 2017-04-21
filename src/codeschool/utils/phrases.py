import random

from codeschool.factories import fake

star_wars_characters = [
    'han solo', 'darth vader', 'c3po', 'r2d2', 'luke skywalker',
    'princess leia', 'jabba', 'obi wan', 'yoda', 'jar jar binks',
]
famous_scientists = [
    # Physicists
    'Einstein', 'Newton', 'Dirac', 'Bohr', 'Rutherford', 'Heisenberg',
    'Curie', 'Langevin', 'Boltzmann',

    # Mathematicians
    'Pythagoras', 'Peano', 'Hilbert', 'Gauss', 'Galois',

    # Computer science
    'Knuth', 'Turing', 'Tim',

    # Biology
    'Darwin', 'Mendel', 'Lamarck', 'Mayr', 'Dobzhansky',
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


def subjective_adjective_phrase(subjectives=None, adjectives=None):
    """
    Return a new subjective-adjective phrase such as "Grumpy Einstein" from a
    list of subjectives and adjectives.
    """
    subjective = random.choice(subjectives or famous_scientists)
    adjective = random.choice(adjectives or adjective_list)
    return '%s %s' % (adjective.title(), subjective)


@is_phase_provider
def random_star_wars_phrase():
    """
    Random phrase based on Star Wars ;-)
    """
    return subjective_adjective_phrase(star_wars_characters)


@is_phase_provider
def random_scientist_phrase():
    """
    Random phrase using important scientists.
    """
    return subjective_adjective_phrase(famous_scientists)


@is_phase_provider
def random_fake_phrase():
    """
    Use fake-factory names.
    """
    return subjective_adjective_phrase([fake.first_name()])


@is_phase_provider
def random_fake_catch():
    """
    Catch phrases
    """
    return fake.catch_phrase()
