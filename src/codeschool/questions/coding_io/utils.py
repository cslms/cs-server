import logging

import ejudge
from annoying.functions import get_config
from markio import parse_markio, Markio

from codeschool.core.models import ProgrammingLanguage

logger = logging.getLogger('codeschool.questions.question_io')


def ejudge_kwargs(lang, timeout):
    """
    Common kwargs for run_code and grade_code functions.
    """

    timeout = timeout or get_config('CODESCHOOL_EXECUTION_TIMEOUT', 10)
    if timeout is None or timeout <= 0:
        raise ValueError('invalid timeout: %r' % timeout)

    sandbox = get_config('CODESCHOOL_SANDBOX', True)
    if sandbox:
        logger.debug('running %s code in sandbox' % lang)
    else:
        logger.warning('running %s code outside sandbox!' % lang)

    if isinstance(lang, ProgrammingLanguage):
        lang = lang.ejudge_ref()

    return dict(
        raises=False,
        sandbox=sandbox,
        timeout=timeout,
        lang=lang
    )


def run_code(source, inputs, lang=None, timeout=None):
    """
    Runs source code with given inputs and return the corresponding IoSpec
    tree.
    """

    return ejudge.run(source, inputs, **ejudge_kwargs(lang, timeout))


def grade_code(source, answer_key, lang=None, timeout=5, stream=False):
    """
    Compare results of running the given source code with the iospec answer
    key.
    """

    if stream is None:
        stream = lang not in ['python', 'pytuga']

    return ejudge.grade(source, answer_key, compare_streams=stream,
                        **ejudge_kwargs(lang, timeout))


def expand_from_code(source, answer_key, lang, timeout=5):
    """
    Expand source code from source.
    """

    # We want to keep all expanded results as is. This both saves CPU and
    # prevents an erroneous answer key source code from producing wrong
    # expansions
    non_expanded = [x for x in answer_key if not x.is_expanded]
    expanded = [(i, x) for i, x in enumerate(answer_key) if x.is_expanded]

    if not non_expanded:
        return answer_key.copy()

    # Compute results from non-expanded results and add the expanded results
    # back to the list
    inputs = answer_key.copy()
    inputs[:] = non_expanded
    results = run_code(source, inputs.inputs(), lang, timeout=timeout)

    for i, x in expanded:
        results.insert(i, x)

    return results


def check_with_code(source, tests, lang, timeout=5, stream=False):
    """
    Compare source code with the results expected on the tests.

    Raises a ValueError if some discrepancy is detected.
    """


def markdown_to_blocks(source):
    """
    Convert a markdown source string to a sequence of blocks.
    """

    # Maybe we'll need a more sophisticated approach that mixes block types
    # and uses headings, markdown blocks and extended markdown syntax. Let us
    # try the simple dumb approach first.
    if isinstance(source, bytes):
        source = source.decode('utf-8')
    block_list = [('markdown', source)]
    return block_list


def blocks_to_markdown(children):
    """
    Convert a sequence of stream children to markdown.
    """

    lines = []
    for child in children:
        if child.block.name == 'markdown':
            lines.append(child.value)
            lines.append('')
        else:
            raise ValueError('cannot convert stream block: %s' %
                             child.block.name)
    return '\n'.join(lines)


def combine_iospecs(left, right):
    """
    Join two IoSpec structures.
    """

    try:
        return left + right
    except TypeError:
        new = left.copy()
        new.extend(right.copy())
        return new


def combine_iospec(tests1, tests2):
    """
    Combine both set of iospec tests test1 and test2.
    """

    result = tests1.copy()
    result.extend(tests2)
    return result


def load_markio(data, parent, update=False, incr_slug=False, validate=True):
    """
    Loads the given Markio data in the parent object.

    Args:
        data:
            A string of data or a Markio object.
        parent:
            The parent page that should hold the CodingIoQuestion resource.
        update
    """

    from codeschool.questions.coding_io.models import CodingIoQuestion

    if isinstance(data, Markio):
        md = data
    else:
        md = parse_markio(data)

    md.validate()
    obj = CodingIoQuestion(title=md.title)
    obj.load_markio_data(md)
    parent.add_child(instance=obj)
    obj.full_clean_all()
    obj.save()
    return obj
