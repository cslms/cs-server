from factory import DjangoModelFactory, LazyAttributeSequence

from . import models


class ProgrammingLanguageFactory(DjangoModelFactory):
    class Meta:
        model = models.ProgrammingLanguage

    ref = LazyAttributeSequence(lambda x: 'lang%s' % x)
    name = LazyAttributeSequence(lambda x: 'Lang-%s' % x)
