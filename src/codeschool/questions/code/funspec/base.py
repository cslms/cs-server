import collections
import inspect
import random
from decimal import Decimal

from iospec.exceptions import BuildError
from faker import Factory
from lazyutils import lazy

fake = Factory.create()


class AnswerKeyTestCase:
    """
    An answer key test case represents the result of execution of a function
    with a set of input arguments.

    It is one of the simplest function-based testing strategies, and is
    implemented in a Funspec module by functions decorated with the
    @answer_key decorator.

    Attributes:
        func (str):
            Name of the tested function.
        args (tuple):
            A tuple of arguments passed to the function.
        result:
            The result of function execution.
        output (str):
            Any eventual print output collected during function execution.
        is_correct (True/False/None):
            Optional argument that can be given to tell if test case is correct
            or not.
    """

    def __init__(self, func, args, result, output='', is_correct=None):
        self.func = func
        self.args = tuple(args)
        self.result = result
        self.output = output
        self.is_correct = is_correct

    def __repr__(self):
        name = self.__class__.__name__
        func = self.func
        inputs = self.args
        output = self.result
        return '%s(%r, %r, %r)' % (name, func, inputs, output)


class Result(collections.Sequence):
    """
    Report the results of Funspec test cases.
    """

    @lazy
    def is_correct(self):
        return all(x.is_correct for x in self.data)

    def __init__(self, data=()):
        self.data = list(data)

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

    def _header(self):
        return ' (%s cases)' % len(self)

    def grade(self, method='ratio'):
        """
        Grade report object by judging the ratio of correct/incorrect answers.

        Args:
            method (str):
                The adopted grading strategy. Can be any of:
                    'ratio':
                        Grade is proportional to the fraction of correct tests.
                    'binary':
                        Users must pass all tests to achieve full grade.
                        Otherwise the grade is zero.

        Returns:
            Returns a decimal grade in the 0-100 range.
        """

        total = len(self.data)
        correct = sum(1 for x in self.data if x.is_correct)

        if method == 'ratio':
            return Decimal(100) * correct / total
        elif method == 'binary':
            return Decimal(100) if total == correct else Decimal(0)
        else:
            raise ValueError('invalid grading method: %r' % method)

    def report(self):
        """
        A human-friendly report.
        """

        print((
            '{classname}{header}:\n'
            '  success: {ratio}%\n'
            '  is correct: {is_correct}\n'
        ).format(
            classname=self.__class__.__name__,
            header=self._header(),
            ratio=self.grade('ratio'),
            is_correct=self.is_correct,
        ))


class ErrorResult(Result):
    """
    A report subclass for reporting critical errors.
    """

    is_correct = False

    def __init__(self, error_type, error_message):
        super().__init__()
        self.error_type = error_type
        self.error_message = error_message

    def _header(self):
        message = self.error_message
        message = '\n'.join('      ' + line for line in message.splitlines())
        return ('\n  error: {error_type}\n'
                '  error_message:\n{message}').format(
            error_type=self.error_type,
            message=message
        )

    def grade(self, method='ratio'):
        return Decimal(0)


class AnswerKeyError(Exception):
    """
    Raised when there is a problem in a answer key definition.
    """


class AnswerKey:
    """
    Wraps a test function.
    """

    def __init__(self, function, name=None):
        self.function = function
        self.name = name or function.__name__
        self._spec = inspect.getfullargspec(self.function)
        self._generators = create_arg_generators(self._spec.annotations)

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)

    def __repr__(self):
        return 'TestFunction(%r)' % getattr(self.function, '__name__',
                                            '<function>')

    def arguments(self, i):
        """
        Return a tuple of valid arguments from the AnswerKey object.
        """

        values = {k: g(i) for k, g in self._generators.items()}
        return tuple(values[arg] for arg in self._spec.args)

    def expand(self, size):
        """
        Return a list of `size` TestCases with the results of running the answer
        key funcftion through all inputs.
        """

        L = []
        for i in range(size):
            args = self.arguments(i)
            result = self.function(*args)
            output = ''
            L.append(AnswerKeyTestCase(self.name, args, result, output))
        return L


class BaseModule(collections.Mapping):
    """
    Base class for FunspecModule and TestModule.
    """

    def __init__(self, data):
        self._data = dict(data)

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __getitem__(self, key):
        return self._data[key]


class FunspecModule(BaseModule):
    """
    Expose the Funspec module as a dictionary of function definitions.
    """

    def __init__(self, data):
        if not isinstance(data, collections.Mapping):
            code, data = data, {}
            exec(code, builtins(), data)
        super().__init__(data)

    def answer_keys(self):
        """
        Return a dictionary with all answer keys in the namespace.
        """

        keys = {}
        for k, v in self.items():
            if getattr(v, '_is_answer_key', False):
                key = keys[k] = AnswerKey(v, k)
        return keys

    def test_cases(self, size):
        """
        Return a dictionary of (function, TestCase) pairs
        """

        data = {}
        for key, answer_key in self.answer_keys().items():
            data[key] = answer_key.expand(size)
        return data


class TestModule(BaseModule):
    """
    Expose functions defined by user/student as a dictionary.
    """

    def __init__(self, data, test_cases):
        self._test_cases = test_cases
        super().__init__(data)

    def test_functions(self):
        """
        Return a dictionary of test functions that should be used during
        unit test evaluation.
        """
        ns = {}
        for name in self._test_cases:
            ns[name] = self._data[name]
        return ns

    def test_cases(self):
        """
        Run all test cases based on results produced by the answer keys.
        """

        functions = self.test_functions()
        data = {}
        for name, cases in self._test_cases.items():
            data[name] = L = []
            function = functions[name]
            for case in cases:
                result = function(*case.args)
                test_case = AnswerKeyTestCase(
                    name, case.args, result,
                    is_correct=case.result == result,
                )
                L.append(test_case)
        return data


class Grader:
    """
    Represents a Funspec testing module.
    """

    _error_message = ''
    funspec = None
    test_cases = None

    def __init__(self, source, num_cases=100):
        self.source = source
        self.num_cases = num_cases

        # Create a code object associated with the module source code
        ns = {}
        try:
            code_obj = compile(self.source, '<funspec>', 'exec')
            try:
                funspec = FunspecModule(code_obj)
                self.test_cases = funspec.test_cases(num_cases)
                self.funspec = funspec
            except BuildError as ex:
                self._error_message = format_error(ex)
        except SyntaxError as ex:
            self._error_message = format_error(ex)

    def test_code(self, source):
        """
        Test the given source code

        Args:
            source (str): input source code string.

        Returns:
            A Report object.
        """

        if self.funspec is None:
            return ErrorResult('module-error', self._error_message)

        try:
            code = compile(source, '<input>', 'exec')
        except SyntaxError as ex:
            return ErrorResult('build-error', format_error(ex))
        try:
            ns = {}
            exec(code, {}, ns)
        except Exception as ex:
            return ErrorResult('build-error', format_error(ex))

        test_mod = TestModule(ns, self.test_cases)
        response = test_mod.test_cases()
        return self.eval_testcases(response)

    def eval_testcases(self, cases):
        """
        Return a feedback that compare the given cases with the cases predicted
        by the funspec module.
        """

        data = []
        for case in cases.values():
            data.extend(case)
        return Result(data)


def format_error(ex):
    """
    Format syntax error into a error_message string.
    """

    return str(ex)


def builtins():
    """
    Return a dictionary of builtins.
    """

    from codeschool.questions.code.funspec import builtins
    return vars(builtins)


class Generator:

    def __init__(self, hint):
        self.hint = hint

    def __call__(self, idx):
        raise NotImplementedError('invalid generator: %r' % self)


class CommandGenerator(Generator):

    def __call__(self, idx):
        pass


class TypeHintGenerator(Generator):

    def __call__(self, idx):
        method = getattr(self, 'from_' + self.hint.__name__)
        return method(idx)

    def from_int(self, idx):
        return random.randint(-1000000, 1000000)

    def from_float(self, idx):
        return random.uniform(-1000000, 1000000)

    def from_str(self, idx):
        return fake.text()


def create_arg_generators(hints):
    """
    Return a dictionary of generator functions from the dictionary of type
    hints.
    """

    generators = {}
    for name, hint in hints.items():
        if isinstance(hint, str):
            generator = CommandGenerator(hint)
        elif isinstance(hint, type):
            generator = TypeHintGenerator(hint)
        elif callable(hint):
            generator = TypeHintGenerator(hint)
        else:
            raise ValueError('unsupported type hint: %r' % hint)
        generators[name] = generator
    return generators


mod_hint = """
@answer_key
def double(x: int):
    return x + x
"""

mod_iospec = """
@answer_key
def double(x: '$int(0, 1000)'):
    return x + x
"""

code_ok = """
def double(x): return 2 * x
"""

code_bad_name = """
def func(x): return x + x
"""

code_bad_func = """
def double(x): return x + 1.5 * x
"""

gh = Grader(mod_hint, 10)
#gi = Grader(mod_iospec, 10)

r = gh.test_code(code_ok)
r.report()
