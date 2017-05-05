from django.utils.translation import ugettext_lazy as _

from codeschool import models


class SpartaActivity(models.Model):
    """
    Represents a sparta activity.
    """

    class Meta:
        verbose_name = _('Sparta Activity')
        verbose_name_plural = _('Sparta Activities')