from django.apps import AppConfig
from django.dispatch import Signal


#: This signal is emitted when a response item finishes its autograde() method
#: successfully and sets the ResponseItem status to STATUS_DONE.
auto_grading = Signal(providing_args=['submission', 'given_grade'])
manual_grading = Signal(providing_args=['submission', 'given_grade'])


class ActivitiesConfig(AppConfig):
    name = 'lms_activities'
