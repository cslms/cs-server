from django import forms
from django.utils.translation import ugettext_lazy as _


class EnrollForm(forms.Form):
    passphrase = forms.CharField(
        max_length=200,
        label=_('Passphrase'),
        help_text=_(
            'This is the secret registration passphrase your teacher provided. '
            'You need to type the correct value in order to register in this classroom.'
        )
    )

    def is_valid_for(self, classroom):
        if self.is_valid():
            passphrase = self.cleaned_data['passphrase']
            if passphrase != classroom.subscription_passphrase:
                self.add_error('passphrase', _('Invalid passphrase'))
                return False
            return True
        return False
