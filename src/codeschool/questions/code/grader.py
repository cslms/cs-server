from django.utils.translation import ugettext_lazy as _

NAME_ERROR_MESSAGE = _('the code must define a {} object')
WRONG_ANSWER_MESSAGE = _('Wrong answer')


def code_errors(grader, test_code, reference_code, name='func'):
    """
    Return a string describing any code error found on the given code.

    If no error is found and the code runs flawlessly, return None.

    Args:
        grader:
            The code responsible for grading a submission.

            This code should define a grade(test, reference) function that
            takes the test function and the reference implementation. Any
            raised exceptions will be captured, converted to text and returned.
        test_code:
            The code submitted for testing.
        reference_code:
            Code with the reference (correct) implementation. It must define
            the same function/object as the test code.
        name:
            Name of the object used for testing in each program.

    Returns:
        A string describing an error or None if the codes executed successfully.
    """

    test = fetch_named_object(test_code, name)
    reference = fetch_named_object(reference_code, name)
    grader = fetch_named_object(grader, 'grader')

    try:
        grader(test, reference)
    except AssertionError as ex:
        return '%s: %s' % (WRONG_ANSWER_MESSAGE, ex)
    except Exception as ex:
        return '%s: %s' % (ex.__class__.__name__, ex)


def fetch_named_object(code, name):
    """
    Execute code and return given object.
    """

    ns = {}
    exec(code, ns)
    try:
        return ns[name]
    except KeyError:
        return 'NameError: ' + NAME_ERROR_MESSAGE.format(name)
