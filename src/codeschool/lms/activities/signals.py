from django.dispatch import Signal


#: This signal is emitted when a submission finishes its autograde() method
#: successfully and sets the Submission status to STATUS_DONE.
#:
#: Args:
#:     submission:
#:         Submission instance.
#:     given_grade (Decimal):
#:         The grade given by the grader.
#:     automatic (bool):
#:         True if grading was performed by the autograder.
submission_graded_signal = Signal(providing_args=['submission', 'given_grade',
                                                  'automatic'])

