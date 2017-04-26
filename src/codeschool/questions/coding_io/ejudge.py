import logging

import ejudge
from annoying.functions import get_config

from codeschool.core.models import ProgrammingLanguage


def ejudge_kwargs(lang, timeout):
    """
    Common kwargs for run_code and grade_code functions.
    """

    timeout = timeout or get_config('CODESCHOOL_EXECUTION_TIMEOUT', 10)
    if timeout is None or timeout <= 0:
        raise ValueError('invalid timeout: %r' % timeout)

    is_testing = get_config('IS_RUNNING_TESTS', False)
    sandbox = get_config('CODESCHOOL_SANDBOX', True) and not is_testing
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


logger = logging.getLogger('codeschool.questions.question_io')
