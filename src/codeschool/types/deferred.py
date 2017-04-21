class Deferred:
    """
    A deferred object.

    It creates a proxy that is converted to the desired object on almost any
    interaction. This only works with pure Python objects since the Deferred
    must have the same C level interface as the real object.
    """

    def __init__(self, cls, *args, **kwargs):
        self.__cls = cls
        self.__args = args
        self.__kwargs = kwargs

    def convert(self):
        # Create proxied object and copy its state back to the Proxy.
        # Changes the object class to the proxied object class.
        obj = self.__cls(*self.__args, **self.__kwargs)

        del self.__cls
        del self.__args
        del self.__kwargs
        self.__dict__.update(obj.__dict__)
        self.__class__ = type(obj)
        assert type(self) is not Deferred

    def __getattr__(self, attr):
        self.convert()
        return self.__getattr__(attr)

    @classmethod
    def _method_factory(cls, attr):
        def method(self, *args, **kwargs):
            self.convert()
            return getattr(self, attr)(*args, **kwargs)
        return method


# Fill methods
for method in ('getitem setitem iter len '
               'repr str '
               'add radd sub rsub mul rmul truediv rtruediv floordiv rfloordiv '
               'eq ne le lt ge gt nonzero bool ').split():
    method = '__%s__' % method
    setattr(Deferred, method, Deferred._method_factory(method))
del method
