import datetime

from annoying.functions import get_config
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _, ugettext as __
from lazyutils import delegate_to
from userena.models import UserenaBaseProfile

from codeschool import models
from codeschool import panels
from codeschool.models import User

strptime = datetime.datetime.strptime


class Profile(UserenaBaseProfile):
    """
    Social information about users.
    """

    class Meta:
        permissions = (
            ('student', _('Can access/modify data visible to student\'s')),
            ('teacher', _('Can access/modify data visible only to Teacher\'s')),
        )

    GENDER_MALE, GENDER_FEMALE = 0, 1

    user = models.OneToOneField(
        User, verbose_name=_('user'),
        unique=True, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='profile',
    )
    school_id = models.CharField(
        _('school id'), max_length=50,
        blank=True, null=True,
        help_text=_(
            'Identification number in your school issued id card.'
        ),
    )
    is_teacher = models.BooleanField(default=False)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    gender = models.SmallIntegerField(
        _('gender'),
        choices=[(GENDER_MALE, _('Male')), (GENDER_FEMALE, _('Female'))],
        blank=True, null=True
    )
    date_of_birth = models.DateField(
        _('date of birth'),
        blank=True, null=True
    )
    website = models.URLField(blank=True, null=True)
    about_me = models.RichTextField(blank=True, null=True)

    # Delegates and properties
    username = delegate_to('user', True)
    first_name = delegate_to('user')
    last_name = delegate_to('user')
    email = delegate_to('user')

    @property
    def age(self):
        if self.date_of_birth is None:
            return None
        today = timezone.now().date()
        birthday = self.date_of_birth
        years = today.year - birthday.year
        birthday = datetime.date(today.year, birthday.month, birthday.day)
        if birthday > today:
            return years - 1
        else:
            return years

    def __str__(self):
        if self.user is None:
            return __('Unbound profile')
        full_name = self.user.get_full_name() or self.user.username
        return __('%(name)s\'s profile') % {'name': full_name}

    def get_full_name_or_username(self):
        name = self.user.get_full_name()
        if name:
            return name
        else:
            return self.user.username

    def get_absolute_url(self):
        return reverse('auth:profile-detail',
                       kwargs={'username': self.user.username})

    # Serving pages
    template = 'cs_auth/profile-detail.jinja2'

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['profile'] = self
        return context

    # Wagtail admin
    panels = [
        panels.MultiFieldPanel([
            panels.FieldPanel('school_id'),
        ], heading='Required information'),

        panels.MultiFieldPanel([
            panels.FieldPanel('nickname'),
            panels.FieldPanel('phone'),
            panels.FieldPanel('gender'),
            panels.FieldPanel('date_of_birth'),
        ], heading=_('Personal Info')),

        panels.MultiFieldPanel([
            panels.FieldPanel('website'),
        ], heading=_('Web presence')),

        panels.RichTextFieldPanel('about_me'),
    ]


@receiver(post_save, sender=models.User)
def create_profile_on_user_save(instance, created, **kwargs):
    """
    Create matching profile when users are created.
    """

    user = instance
    if created and user.username != 'AnonymousUser':
        profile, _ = Profile.objects.get_or_create(user=user)
        if get_config('CODESCHOOL_USERNAME_IS_SCHOOL_ID', False):
            profile.school_id = user.username
        profile.save()


models.User.get_absolute_url = lambda x: reverse(
    'auth:profile-detail', args=(x.username,))
