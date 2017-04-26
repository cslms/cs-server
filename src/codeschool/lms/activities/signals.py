from django.dispatch import Signal


#: This signal is emitted when a response item finishes its autograde() method
#: successfully and sets the ResponseItem status to STATUS_DONE.
auto_grading = Signal(providing_args=['submission', 'given_grade'])
manual_grading = Signal(providing_args=['submission', 'given_grade'])


#: This signal is emitted when a submission finishes its autograde() method
#: successfully and sets the Submission status to STATUS_DONE.
#:
#: Args:
#:     submission:
#:         Submission instance.
#:     automatic (bool):
#:         True if grading was performed by the autograder.
submission_graded_signal = Signal(providing_args=['submission', 'given_grade',
                                                  'automatic'])

#: This signal is emitted for the first submission sent for some specific
#: activity.
#:
#: Args:
#:     submission:
#:         Submission instance.
first_submission_signal = Signal(providing_args=['submission'])


#: This signal is emitted when a graded submission is the first *correct*
#: submission for some specific activity.
#:
#: Args:
#:     submission:
#:         Submission instance.
first_correct_submission_signal = Signal(providing_args=['submission'])
