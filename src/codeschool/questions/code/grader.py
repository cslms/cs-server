import os

import tempfile
import traceback

try:
    from django.utils.translation import ugettext_lazy as _
except ImportError:
    _ = lambda x: x

NAME_ERROR_MESSAGE = _('the code must define a {} object')
WRONG_ANSWER_MESSAGE = _('Wrong answer')


class FetchObjectError(Exception):
    """
    Error raised when object cannot be fetched from program.
    """


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

    try:
        test = fetch_named_object(test_code, name, 'code.py')
        reference = fetch_named_object(reference_code, name, 'reference.py')
        grader = fetch_named_object(grader, 'grader', 'grader.py')
    except FetchObjectError as ex:
        raised = ex.args[0]
        return 'RuntimeError (%s): %s' % (raised.__class__.__name__, raised)

    print(test, reference, grader)

    try:
        grader(test, reference)
    except AssertionError as ex:
        return '%s: %s' % (WRONG_ANSWER_MESSAGE, ex)
    except Exception as ex:
        return '%s: %s' % (ex.__class__.__name__, ex)


def fetch_named_object(source, obj_name, file_name='default.py'):
    """
    Execute code and return given object.
    """

    ns = {}

    tmp_dir = tempfile.mkdtemp()
    try:
        tmp_file = os.path.join(tmp_dir, file_name)

        with open(tmp_file, 'w', encoding='utf8') as F:
            F.write(source)

        try:
            code = compile(source, tmp_file, 'exec', dont_inherit=True)
            exec(code, ns)
        except Exception as ex:
            raise FetchObjectError(traceback.format_exc())
    finally:
        for f in os.listdir(tmp_dir):
            os.unlink(os.path.join(tmp_dir, f))
        os.rmdir(tmp_dir)

    try:
        return ns[obj_name]
    except KeyError:
        raise FetchObjectError(
            NameError('object %r is not defined' % obj_name))
