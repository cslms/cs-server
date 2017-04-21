import model_reference
import srvice
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from codeschool import models
from codeschool.utils import LazyManager

courses = LazyManager('courses', 'course')


class CourseList(models.RoutablePageMixin, models.Page):
    """
    A list of courses
    """

    # Serving pages
    template = 'courses/list.jinja2'

    def get_context(self, request, **kwargs):
        return dict(
            super().get_context(request, **kwargs),
            course_list=courses.for_user(request.user),
            open_courses=courses.open_for_user(request.user),
        )

    @srvice.route(r'subscribe/$')
    def serve_subscribe_action(self, client):
        context = self.get_context(client.request)
        html_data = render_to_string('courses/subscribe-dialog.jinja2', context,
                                     request=client.request)
        client.dialog(html=html_data)

    # Wagtail admin
    parent_page_types = []
    subpage_types = ['courses.Course']
    content_panels = models.Page.content_panels + [
        # panels.InlinePanel(
        #     'time_slots',
        #     label=_('Time slots'),
        #     help_text=_('Define when the weekly classes take place.'),
        # ),
    ]
    settings_panels = models.Page.settings_panels + [
        # panels.MultiFieldPanel([
        #     panels.FieldPanel('weekly_lessons'),
        #     panels.FieldPanel('is_public'),
        # ], heading=_('Options')),
        # panels.MultiFieldPanel([
        #     panels.FieldPanel('accept_subscriptions'),
        #     panels.FieldPanel('subscription_passphrase'),
        # ], heading=_('Subscription')),
    ]


@model_reference.factory('course-list')
def make_courses_list():
    """
    Creates the default site-wide courses list.

    All course pages should be children of this page.
    """

    parent_page = model_reference.load('root-page')
    courses_list = CourseList(
        title=_('Courses'),
        slug='courses',
    )
    return parent_page.add_child(instance=courses_list)
