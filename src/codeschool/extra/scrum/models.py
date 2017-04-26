import datetime

from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now

from codeschool import models
from codeschool import panels

one_week = datetime.timedelta(days=7)


# Validators
def non_null(x):
    return x >= 1


class ScrumProject(models.RoutablePageMixin,
                   models.Page):
    """
    A simple scrum project.
    """

    description = models.RichTextField()
    members = models.ManyToManyField(models.User)
    workday_duration = models.IntegerField(default=2)

    @property
    def backlog_tasks(self):
        return self.tasks.filter(status=Task.STATUS_BACKLOG)

    # Public functions
    def finish_date(self):
        """
        Return the finish date for the last sprint.
        """
        try:
            return self.sprints.order_by('due_date').last().due_date

        except Sprint.DoesNotExist:
            return now()

    # Serving pages
    @models.route(r'^sprints/new/$')
    def serve_new_sprint(self, request):
        return serve_new_sprint(request, self)

    @models.route(r'^sprints/(?P<id>[0-9]+)/$')
    def serve_view_sprint(self, request, id=None, *args, **kwargs):
        print(args)
        print(kwargs)
        sprint = get_object_or_404(Sprint, id=id)
        return serve_view_sprint(request, self, sprint)

    @models.route(r'^sprints/$')
    def serve_list_sprint(self, request, *args, **kwargs):
        return serve_list_sprints(request, self)

    # Wagtail specific
    template = 'scrum/project.jinja2'

    content_panels = models.Page.content_panels + [
        panels.FieldPanel('description'),
        panels.FieldPanel('workday_duration'),
    ]


class Sprint(models.Model):
    """
    A sprint
    """

    project = models.ForeignKey(ScrumProject, related_name='sprints')
    description = models.RichTextField(blank=True)
    start_date = models.DateTimeField()
    due_date = models.DateTimeField()
    duration_weeks = models.PositiveIntegerField(default=1,
                                                 validators=[non_null])

    def next_start_date(self, date=None):
        """
        Return the next valid date that the sprint could start after the given.

        If no arguments are given, consider the current time.
        """

        date = date or now()
        return date

    def attach(self, project, commit=True):
        """
        Associate sprint to project, updating required values.
        """

        date = project.finish_date()
        self.project = project
        self.start_date = self.next_start_date(date)
        self.due_date = self.start_date + one_week * self.duration_weeks
        if commit:
            self.save()


class TaskQuerySet(models.QuerySet):

    def todo(self):
        return self.filter(status=Task.STATUS_TODO)

    def doing(self):
        return self.filter(status=Task.STATUS_DOING)

    def done(self):
        return self.filter(status=Task.STATUS_DONE)


class Task(models.Model):
    """
    A task that can be on the backlog or on a sprint.
    """

    STATUS_BACKLOG = 0
    STATUS_TODO = 1
    STATUS_DOING = 2
    STATUS_DONE = 3
    STATUS = models.Choices(
        (STATUS_BACKLOG, 'backlog'),
        (STATUS_TODO, 'todo'),
        (STATUS_DOING, 'doing'),
        (STATUS_DONE, 'done'),
    )
    sprint = models.ForeignKey(Sprint, related_name='tasks')
    project = models.ForeignKey(ScrumProject, related_name='tasks')
    status = models.StatusField()
    created_by = models.ForeignKey(models.User, related_name='+')
    assigned_to = models.ManyToManyField(models.User, related_name='+')
    description = models.RichTextField()
    duration_hours = models.IntegerField()
    objects = TaskQuerySet.as_manager()


#
# Forms
#
class SprintForm(forms.ModelForm):

    class Meta:
        model = Sprint
        fields = ['description', 'duration_weeks']


#
# Views
#
def serve_new_sprint(request, project):
    if request.method == 'POST':
        form = SprintForm(request.POST)
        if form.is_valid():
            form.instance.attach(project)
            return redirect('../%s/' % form.instance.id)
    else:
        form = SprintForm()
    context = project.get_context(request)
    context['form'] = form
    return render(request, 'scrum/new-sprint.jinja2', context)


def serve_view_sprint(request, project, sprint):
    context = project.get_context(request)
    context.update(
        sprint=sprint,
    )
    return render(request, 'scrum/sprint-detail.jinja2', context)


def serve_list_sprints(request, project):
    context = project.get_context(request)
    context.update(
        sprints=project.sprints.order_by('start_date'),
    )
    return render(request, 'scrum/list-sprints.jinja2', context)
