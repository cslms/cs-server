from collections import OrderedDict

from markio import Markio, parse_markio

from codeschool.core import get_programming_language
from codeschool.questions.coding_io.utils import markdown_to_blocks, \
    blocks_to_markdown


def load_markio(data, parent, update=False, incr_slug=False, validate=True):
    """
    Creates a CodingIoQuestion object from a Markio object or source
    string and saves the resulting question in the database.

    Args:
        source:
            A string with the Markio source code.
        parent:
            The parent page object.

    Returns:
        A CodingIoQuestion instance.
    """

    from codeschool.questions.coding_io.models import CodingIoQuestion

    if isinstance(data, Markio):
        md = data
    else:
        md = parse_markio(data)

    md.validate()
    question = CodingIoQuestion(title=md.title)
    update_markio_data(question, md)
    parent.add_child(instance=question)
    question.full_clean_all()
    question.save()
    return question


def import_markio_from_path(path, parent):
    """
    Like load_markio(), but reads source from the given file path.
    """

    with open(path) as F:
        data = parse_markio(F)
    return load_markio(data, parent)


def update_markio_data(question, data):
    """
    Update question parameters from Markio file.
    """

    md = data if hasattr(data, 'title') else parse_markio(data)

    # Load simple data from markio
    question.title = md.title or question.title
    question.short_description = (md.short_description or
                                  question.short_description)
    question.timeout = md.timeout or question.timeout
    question.author_name = md.author or question.author_name
    question.pre_tests_source = md.tests_source or question.pre_tests_source
    question.post_tests_source = md.hidden_tests_source
    if md.language is not None:
        question.language = get_programming_language(md.language)
    if md.points is not None:
        question.points_total = md.points
    if md.stars is not None:
        question.starts_total = md.stars

    # Load main description
    question.body = markdown_to_blocks(md.description)

    # Add answer keys
    answer_keys = OrderedDict()
    for (lang, answer_key) in md.answer_key.items():
        language = get_programming_language(lang)
        key = question.answers.create(question=question,
                                      language=language,
                                      source=answer_key)
        answer_keys[lang] = key
    for (lang, placeholder) in md.placeholder.items():
        if placeholder is None:
            question.default_placeholder = placeholder
        try:
            answer_keys[lang].placeholder = placeholder
        except KeyError:
            language = get_programming_language(lang)
            question.answers.create(language=language,
                                    placeholder=placeholder)
    question.__answers = list(answer_keys.values())
    question.answers = question.__answers


def dump_markio(question):
    """
    Serializes question into a string of Markio source.
    """

    md = Markio(
        title=question.title,
        author=question.author_name,
        timeout=question.timeout,
        short_description=question.short_description,
        description=blocks_to_markdown(question.body),
        tests=question.pre_tests_source,
    )

    for key in question.answers.all():
        if key.source:
            md.answer_key.add(key.source, key.language.ejudge_ref())
        if key.get_placeholder:
            md.placeholder.add(key.get_placeholder,
                               key.language.ejudge_ref())

    return md.source()
