from django.core.exceptions import ValidationError
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as __, ugettext as _
from iospec import parse as parse_iospec, IoSpecSyntaxError


def timeout_validator(timeout):
    if timeout <= 0:
        raise ValidationError(_('Timeout must be strictly positive.'))


def positive_integer_validator(size):
    if size <= 0:
        raise ValidationError(_('Test size must be strictly positive'))


def iospec_source_validator(iospec):
    if iospec:
        try:
            parse_iospec(iospec)
        except IoSpecSyntaxError as ex:
            raise ValidationError(_('Invalid IoSpec: %(msg)s') % {'msg': ex})


def inconsistent_testcase_error(test1, test2, field):
    ns = {
        'lang1': test1.language,
        'lang2': test2.language,
    }
    msg = _('%(lang1)s and %(lang2)s are producing different results') % ns
    public_field = field.replace('_expanded', '')
    return ValidationError({public_field: msg})


def inconsistent_iospec_error(answer_key, ref, obtained):
    for ref, obtained in zip(ref, obtained):
        if ref != obtained:
            break
    ref = escape(ref.source())
    obtained = escape(obtained.source())

    return ValidationError({
        'source': mark_safe(INCONSISTENT_ERROR % locals())
    })


def invalid_question_iospec_error(question, ex):
    return ValidationError(_(
        'cannot register answer key for question with invalid iospec: %(msg)s.'
    ) % {'msg': str(ex)})


def reference_code_execution_error(key, ex):
    return ValidationError({
        'source': _(
            'Error on reference code execution: %(error)s'
        ) % {'error': str(ex)},
    })


def invalid_related_answer_key_error(key, ex):
    field, messages = ex.args[0].popitem()
    msg = _(
        'invalid answer key: "%(lang)s":%(field)s:\n'
        '%(message)s'
    ) % {'lang': key.language,
         'field': field,
         'message': messages}
    raise ValidationError({'answers': [msg]})


ERROR_TEMPLATE = __("""
<!-- (translators) tags really don't match! -->
Errors produced when executing program with code</p>
<pre class="error-message" style="margin-left: 2em">%(iospec)s</pre>
<p class="error-message">Error message:</p>
<pre class="error-message" style="margin-left: 2em">%(error)s</pre>
<p class="hidden">
""")
INCONSISTENT_ERROR = __("""
<!-- (translators) tags really don't match! -->
Code returned an inconsistent response</p>
<p class="error-message">Expected:</p>
<pre class="error-message" style="margin-left: 2em">%(ref)s</pre>
<p class="error-message">Obtained:</p>
<pre class="error-message" style="margin-left: 2em">%(obtained)s</pre>
<p style="display: none">
""")
