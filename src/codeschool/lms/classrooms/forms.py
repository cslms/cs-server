from django import forms
from django.utils.translation import ugettext_lazy as _


class PassPhraseForm(forms.Form):
    passphrase = forms.CharField(
        max_length=200,
        label=_('Pass-phrase'),
        help_text=_(
            'This is the secret registration pass-phrase the teacher provided.'
        )
    )