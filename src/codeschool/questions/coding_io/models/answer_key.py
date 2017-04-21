from html import escape

from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from modelcluster.fields import ChildObjectsDescriptor

from codeschool import models, panels
from codeschool.core.models import ProgrammingLanguage
from codeschool.questions.coding_io.models import CodingIoQuestion
from codeschool.utils import md5hash


class ChildDescriptor(ChildObjectsDescriptor):

    def __get__(self, instance, instance_type=None):
        if instance is None:
            return self
        else:
            manager = super().__get__(instance, instance_type)
            return AnswerKeyRelatedManager(manager)


# class AnswerKeyQuerySet():
#     """
#     Base functionality common to regular querysets and the fake related
#     querysets used by django-model-cluster
#     """
#
#     def language(self, language):
#         """
#         Filter answer keys by language.
#         """
#
#         return self.filter(language=language)
#
#
#     def expand_all(self, iospec):
#         """
#         Return a expanded IoSpec object obtained by running the reference
#         program for all elements that define a source.
#         """
#
#         if not iospec.is_expanded:
#             iospec = iospec.copy()
#             iospec.expand_inputs()
#
#         return [key.expand(iospec) for key in self.has_program()]
#
#
# class AnswerKeyFakeQuerySet(AnswerKeyQuerySetBase, FakeQuerySet):
#     """
#     Fake queryset used in django-model-cluster.
#     """
#
#     def filter(self, **kwargs):
#         value = super().filter(**kwargs)
#         value.__class__ = AnswerKeyFakeQuerySet
#         return value
#
#     def exclude(self, **kwargs):
#         value = super().exclude(**kwargs)
#         value.__class__ = AnswerKeyFakeQuerySet
#         return value
#
#     def order_by(self, *fields):
#         value = super().order_by(*fields)
#         value.__class__ = AnswerKeyFakeQuerySet
#         return value
#
#
# class AnswerKeyRelatedManager(AnswerKeyQuerySetBase, collections.Mapping):
#     _NOT_GIVEN = object()
#
#     def __init__(self, manager):
#         self._manager = manager
#         self._manager_cls = type(manager)
#
#     def __getitem__(self, language):
#         return self.get(language=get_programming_language(language))
#
#     def __iter__(self):
#         for lang_id in self.values_list('language', flat=True):
#             yield ProgrammingLanguage.objects.get(id=lang_id)
#
#     def __len__(self):
#         return self.count()
#
#     def __getattr__(self, attr):
#         try:
#             value = getattr(self._manager, attr)
#         except AttributeError:
#             raise AttributeError(attr)
#
#         if not callable(value):
#             return self._wrap_value(value)
#
#         def method(*args, **kwargs):
#             result = value(*args, **kwargs)
#             return self._wrap_value(result)
#
#         return method
#
#     def _wrap_value(self, value):
#         cls = type(value)
#         if value is self._manager:
#             return self
#         elif cls is FakeQuerySet:
#             value.__class__ = AnswerKeyFakeQuerySet
#         elif cls is self._manager_cls:
#             value = AnswerKeyRelatedManager(value)
#         return value
#
#     def is_complete(self):
#         """
#         Return True if an answer key item exists for all valid programming
#         languages.
#         """
#
#         refs = self.values_list('language__ref', flatten=True)
#         all_refs = ProgrammingLanguage.objects.values('ref', flatten=True)
#         return set(all_refs) == set(refs)
#
#
# class AnswerKeyQueryset(AnswerKeyQuerySetBase, models.QuerySet):
#     pass
#
#
# class AnswerKeyManager(models.Manager):
#     use_for_related_fields = True
#
#
# AnswerKeyManager = AnswerKeyManager.from_queryset(AnswerKeyQueryset)


def check_syntax(source, lang):
    """
    Raises a SyntaxError if source code is invalid in the given language.
    """

    if lang == 'python':
        compile(source, '<input>', 'exec')
    else:
        # FIXME: implement this in ejudge.
        pass


class AnswerKey(models.Model):
    """
    Represents an answer to some question given in some specific computer
    language plus the placeholder text that should be displayed.
    """

    NULL_SOURCE_HASH = md5hash('')

    class ValidationError(Exception):
        pass

    class Meta:
        verbose_name = _('answer key')
        verbose_name_plural = _('answer keys')
        unique_together = [('question', 'language')]

    question = models.ParentalKey(
        CodingIoQuestion,
        related_name='answers'
    )
    language = models.ForeignKey(
        ProgrammingLanguage,
        related_name='+',
    )
    source = models.TextField(
        _('answer source code'),
        blank=True,
        help_text=_(
            'Source code for the correct answer in the given programming '
            'language.'
        ),
    )
    placeholder = models.TextField(
        _('placeholder source code'),
        blank=True,
        help_text=_(
            'This optional field controls which code should be placed in '
            'the source code editor when a question is opened. This is '
            'useful to put boilerplate or even a full program that the '
            'student should modify. It is possible to configure a global '
            'per-language boilerplate and leave this field blank.'
        ),
    )
    source_hash = models.CharField(
        max_length=32,
        default=NULL_SOURCE_HASH,
        help_text=_('Hash computed from the reference source'),
    )
    error_message = models.TextField(
        _('error message'),
        blank=True,
        help_text=_(
            'If an error is found on post-validation, an error message is '
            'stored in here.'
        )
    )

    def __repr__(self):
        return '<AnswerKey: %s>' % self

    def __str__(self):
        try:
            title = self.question.title
        except:
            title = '<untitled>'
        return '%s (%s)' % (title, self.language)

    def save(self, *args, **kwargs):
        self.source_hash = md5hash(self.source)
        super().save(*args, **kwargs)

    def clean(self):
        try:
            check_syntax(self.source, lang=self.language.ejudge_ref())
        except SyntaxError as ex:
            msg = _('Invalid syntax: %(msg)') % {'msg': str(ex)}
            raise ValidationError({'source': msg})
        super().clean()

        # Validation is async:
        #
        # We first run basic validations in the foreground and later attempt
        # at more detailed validations that requires us to run source code (and
        # thus possibly wait a long time).
        #
        # If this later validation step encounters errors, it saves them on
        # the model instance. The next time the model runs, we can re-raise
        # them on the interface. The user has an option to bypass these checks.
        # Changing the code or the iospec entries should expire these
        # errors.
        if self.error_message and not self.is_ignoring_validation_errors():
            raise ValidationError({'source': mark_safe(self.error_message)})

    def is_ignoring_validation_errors(self):
        """
        True to ignore errors found in post-validation.
        """

        return self.question.ignore_validation_errors

    def set_error_message(self, message):
        """
        Saves error message.
        """

        try:
            self.error_message = message.__html__()
        except AttributeError:
            self.error_message = escape(message)

    def has_changed_source(self):
        """
        Return True if source is not consistent with its hash.
        """

        return self.source_hash != md5hash(self.source)

    #
    #
    #

    def single_reference(self):
        """
        Return True if it is the only answer key in the set that defines a
        source attribute.
        """

        if not self.source:
            return False

        try:
            return self.question.answers.has_program().get() == self
        except self.DoesNotExist:
            return False

    # Wagtail admin
    panels = [
        panels.FieldPanel('language'),
        panels.FieldPanel('source'),
        panels.FieldPanel('placeholder'),
    ]
