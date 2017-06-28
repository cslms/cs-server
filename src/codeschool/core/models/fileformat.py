from codeschool import models


class SourceFormatQuerySet(models.QuerySet):

    def supported(self):
        """
        Filter-in only the supported formats.
        """

        return self.filter(is_supported=True)

    def unsupported(self):
        """
        Filter-out the supported formats.
        """

        return self.filter(is_supported=False)


class FileFormat(models.Model):
    """
    Represents a source file format.

    These can be programming languages or some specific data format.
    """

    ref = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=140)
    comments = models.TextField(blank=True)
    is_binary = models.BooleanField(default=False)
    is_language = models.BooleanField(default=False)
    is_supported = models.BooleanField(default=False)
    objects = models.Manager.from_queryset(SourceFormatQuerySet)()

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('name', kwargs.get('ref', 'unnamed format').title())
        super().__init__(*args, **kwargs)

    def ace_mode(self):
        """
        Return the ace mode associated with the format.
        """

        return ACE_ALIASES.get(self.ref, self.ref)

    def pygments_mode(self):
        """
        Returns the Pygments mode associated with the format.
        """

        return self.ref

    def ejudge_ref(self):
        """
        A valid reference for the language in the ejudge framework.
        """

        return self.ref

    def __str__(self):
        return self.name


class ProgrammingLanguage(FileFormat):
    """
    Represents a programming language in codeschool.
    """

    class Meta:
        proxy = True

    objects = models.QueryManager.from_queryset(models.QuerySet)(
        is_supported=True,
        is_language=True,
    )
    unsupported = models.QueryManager(is_supported=False, is_language=True)
    supported = models.QueryManager(is_supported=True, is_language=True)

    @classmethod
    def get_language(cls, ref, raises=True):
        """
        Return the programming language object from the given ref.

        If raises is False, return None instead of raising a DoesNotExist
        exception if the requested language does not exist.
        """

        # We save ProgrammingLanguage instances in a cache for fast access.
        # This way we avoid unnecessary trips to the db.
        ref = FORMAT_ALIASES.get(ref, ref)
        lang = PROGRAMMING_LANGUAGES_CACHE.get(ref)
        if lang is not None:
            return lang

        # Language is not in cache. Fetch it and save it on second use.
        try:
            if isinstance(ref, int) or ref.isdigit():
                ref = int(ref)
                lang = cls.objects.get(pk=ref)
            else:
                lang = cls.objects.get(ref=ref)
            PROGRAMMING_LANGUAGES_CACHE[ref] = lang
            return lang
        except cls.DoesNotExist:
            if raises:
                raise cls.DoesNotExist('invalid language: %r' % ref)
            return cls.objects.create(
                ref=ref,
                name=ref.title(),
                is_language=True,
                is_supported=False,
                comments='*automatically created*'
            )

    @classmethod
    def get_or_create_language(cls, ref, name=None):
        """
        Return language with the given ref, and create it if it does not exist.
        """

        try:
            return cls.get_language(ref)
        except cls.DoesNotExist:
            return cls.unsupported.create(ref=ref, name=name or ref)[0]

    def save(self, *args, **kwargs):
        self.is_language = True
        super().save(*args, **kwargs)


#
# These functions associate data with specific programming languages and their
# default support in codeschool.
#
def format_processor(func):
    """
    Process each class of formats using the process function.

    The function should take a list of dictionaries that represent keyword
    arguments that could be passed to the SourceFormat constructor.
    """

    def process(lst, **kwargs):
        lst = (x.partition(':') for x in lst)
        lst = ((ref, name) for (ref, _, name) in lst)
        lst = (dict(kwargs, ref=ref, name=name) for (ref, name) in lst)
        return func(list(lst))

    # Binary formats
    process([
        'pdf:PDF',
        'rtf:Rich text format',
        'docx:Microsoft Word',
        'doc:Microsoft Word (legacy)',
        'odt:Open document text',
    ], is_binary=True)

    # Text formats
    process([
        'markdown:Markdown',
        'text:Plain Text',
        'html:HTML',
        'css:CSS',
        'latex:LaTeX',
        'tex:TeX',
    ])

    # Non-supported languages
    process([
        'ruby:Ruby',
        'java:Java',
        'javascript:Javascript',
        'perl:Perl',
        'haskell:Haskell',
        'julia:Julia',
        'go:Go',
    ], is_language=True)

    # Supported programming languages
    process([
        'pytuga:Pytuguês',
        'python:Python 3.5',
        'python2:Python 2.7',
        'c:C99 (gcc compiler)',
        'cpp:C++11',
    ], is_language=True, is_supported=True)


def formats_yaml_dump():
    """
    Return a string YAML dump with fixture data for all formats.
    """

    dump = []

    def process(lst, **kwargs):
        def subs(v):
            if isinstance(v, bool):
                return str(v).lower()
            return repr(v)

        for kwargs in lst:
            ref = kwargs.pop('ref')
            name = kwargs.pop('name')
            dump.append(
                '- model: cs_core.fileformat\n'
                '  pk: %r\n'
                '  fields:\n'
                '    name: %r\n' % (ref, name) +
                ''.join('    %s: %s\n' % (k, subs(v))
                        for k, v in kwargs.items())
            )

    format_processor(process)
    return '\n'.join(dump)


def init_file_formats():
    """
    Initialize all file formats and save them to the db.
    """

    def process(lst):
        for kwargs in lst:
            if not FileFormat.objects.filter(ref=kwargs['ref']):
                FileFormat.objects.create(**kwargs)

    format_processor(process)


def init_format_aliases():
    """
    Add a few more aliases to the format aliases.
    """

    def process(lst):
        for data in lst:
            FORMAT_ALIASES[data['name']] = data['ref']
            FORMAT_ALIASES[data['name'].lower()] = data['ref']
            FORMAT_ALIASES[data['name'].lower().replace(' ', '')] = data['ref']

    format_processor(process)


# Compute format aliases
PROGRAMMING_LANGUAGES_CACHE = {}
FORMAT_ALIASES = {
    'python3': 'python',
    'py3': 'python',
    'py2': 'python2',
    'gcc': 'c',
    'g++': 'cpp',
}
ACE_ALIASES = {
    'c': 'c_cpp',
    'cpp': 'c_cpp',
    'python2': 'python',
    'pytuga': 'python',
}

init_format_aliases()
