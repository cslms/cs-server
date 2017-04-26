import pytest


class ClassTesterMeta(type):
    """
    Metaclass for ClassTester.
    """

    def __init__(cls, name, bases, ns):
        super().__init__(name, bases, ns)
        cls._create_instance_list_fixture()
        cls._create_fixtures_for_base_args()

    def _create_instance_list_fixture(cls):
        fixtures = ['obj']
        for name, value in vars(cls).items():
            if getattr(value, '__is_instance_fixture', False):
                fixtures.append(name)

        @pytest.mark.usefixtures(*fixtures)
        def instances(request):
            print(request.__dict__)
            return []

        cls.instances = instances

    def _create_fixtures_for_base_args(cls):
        methods = dir(cls)
        base_args = [m[11:] for m in methods if m.startswith('base_args__')]
        base_kwargs = [m[13:]
                       for m in methods if m.startswith('base_kwargs__')]

        # Fill missing kwargs and args
        for arg in base_args:
            if arg not in base_kwargs:
                setattr(cls, 'base_kwargs__' + arg, {})
        for arg in base_kwargs:
            if arg not in base_args:
                setattr(cls, 'base_args__' + arg, ())

        # Create fixtures
        def make_fixture(arg):
            args_attr = 'base_args__' + arg
            kwargs_attr = 'base_kwargs__' + arg

            def fixture(self, cls):
                args = getattr(self, args_attr)
                kwargs = getattr(self, kwargs_attr)
                return cls(*args, **kwargs)

            fixture.__name__ = arg
            return pytest.fixture(fixture)

        for arg in set(base_args + base_kwargs):
            if not hasattr(cls, arg):
                fixture = make_fixture(arg)
                setattr(cls, arg, fixture)

    def __temp(cls, name, bases, ns):
        super().__init__(name, bases, ns)

        for attr in dir(cls):
            if attr.endswith('_factory'):
                fixture_name = attr[:-8]
                if not hasattr(cls, fixture_name):
                    fixture = cls._make_fixture(fixture_name)
                    setattr(cls, fixture_name, fixture)

    def _make_fixture(cls, name):
        factory = getattr(cls, name + '_factory')

        def fixture(self):
            return factory.create()

        fixture.__name__ = name
        return pytest.fixture(fixture)


def instance_fixture(func):
    """
    Mark function as an instance fixture.

    It marks function as a fixture and also applies pytest.mark.instance_fixture
    """

    func = pytest.fixture(func)
    func = pytest.mark.instance_fixture(func)
    func.__is_instance_fixture = True
    return func


class ClassTester(metaclass=ClassTesterMeta):
    """
    Tests around a base class.
    """

    base_cls = None
    base_args = ()
    base_kwargs = {}
    base_args__other = ()
    base_kwargs__other = {}
    base_repr = None

    @pytest.fixture
    def args_other(self):
        return self.base_args__other

    @pytest.fixture
    def kwargs_other(self):
        return self.base_kwargs__other

    @pytest.fixture
    def other(self, cls, args_other, kwargs_other):
        return cls(*args_other, **kwargs_other)

    @pytest.fixture
    def obj(self, cls, args, kwargs):
        return cls(*args, **kwargs)

    @pytest.fixture
    def cls(self):
        if self.base_args is None:
            raise RuntimeError('please define the base_cls attribute')
        return self.base_cls

    @pytest.fixture
    def args(self):
        return self.base_args

    @pytest.fixture
    def kwargs(self):
        return self.base_kwargs

    @pytest.fixture
    def invariants(self):
        inv_names = [
            name for name in dir(self)
            if not name.startswith('test_') and name.endswith('_invariant')
        ]
        return [getattr(self, attr) for attr in inv_names]

    @pytest.fixture
    def tol(self):
        return 1e-5

    def random_obj(self):
        """
        A random object.
        """

        return self.base_cls(*self.random_args())

    def random_args(self):
        """
        A random valid argument used to instantiate a random object
        """

        raise NotImplementedError

    def test_basic_sanity_check(self, obj, cls):
        if self.base_repr is not None:
            assert repr(obj) == self.base_repr
        assert isinstance(obj, cls)
