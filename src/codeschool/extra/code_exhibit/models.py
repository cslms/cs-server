import bricks
from django import forms
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from codeschool import models
from codeschool import panels
from codeschool.lms.activities.models import Activity


class CodeExhibit(Activity):
    """
    Students can publish code + an associated image (think about turtle art or
    Processing) and then vote in the best submissions.
    """

    class Meta:
        verbose_name = _('Code exhibit')
        verbose_name_plural = _('Code exhibits')

    description = models.RichTextField()
    language = models.ForeignKey(
        'core.ProgrammingLanguage',
        on_delete=models.PROTECT,
    )

    def get_submit_form(self, *args, **kwargs):
        class ExhibitEntryForm(forms.ModelForm):

            class Meta:
                model = ExhibitEntry
                fields = ['name', 'image', 'source']

        return ExhibitEntryForm(*args, **kwargs)

    # Page rendering and views
    template = 'code_exhibit/code_exhibit.jinja2'

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['entries'] = self.entries.all()
        return context

    @bricks.route(r'^get-form/$')
    def route_submit_form(self, client):
        form = self.get_submit_form()
        context = {'form': form, 'language': self.language}
        html = render_to_string('code_exhibit/submit.jinja2', context,
                                request=client.request)
        client.dialog(html=html)

    @models.route(r'^submit-entry/$')
    def route_submit(self, request):
        if request.method == 'POST':
            print(request.POST)
            form = self.get_submit_form(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                print('saving model', instance)
                instance.user = request.user
                instance.exhibit = self
                instance.save()
            else:
                print(form.errors)
        return redirect(self.get_absolute_url())

    # Wagtail Admin
    content_panels = Activity.content_panels + [
        panels.FieldPanel('description'),
        panels.FieldPanel('language'),
        panels.InlinePanel('entries'),
    ]


#
# Submissions
#
class ExhibitEntryQuerySet(models.QuerySet):
    pass


class ExhibitEntry(models.ClusterableModel):
    """
    Each user submission
    """

    class Meta:
        unique_together = [('user', 'exhibit')]

    exhibit = models.ParentalKey(CodeExhibit, related_name='entries')
    user = models.ForeignKey(models.User, related_name='+',
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    source = models.TextField()
    image = models.ImageField(upload_to='images/code_exhibit/')
    # image = models.FileField(upload_to='images/code_exhibit/')
    votes_from = models.ManyToManyField(models.User, related_name='+')
    num_votes = models.IntegerField(default=int)
    objects = ExhibitEntryQuerySet.as_manager()

    def vote(self, user):
        """
        Register a vote from user.
        """

        if not self.votes_from.filter(id=user.id).count():
            self.votes_from.add(user)
            self.num_votes += 1
            self.save(update_fields=['num_votes'])

    def unvote(self, user):
        """
        Remove a vote from user.
        """

        if self.votes_from.filter(id=user.id).count():
            self.votes_from.remove(user)
            self.num_votes -= 1
            self.save(update_fields=['num_votes'])

    def icon_for_user(self, user):
        if user in self.votes_from.all():
            return 'star'
        return 'start_border'

    # Wagtail admin
    panels = [
        panels.FieldPanel('user'),
        panels.FieldPanel('source'),
        panels.FieldPanel('image'),
        panels.FieldPanel('num_votes'),
    ]
