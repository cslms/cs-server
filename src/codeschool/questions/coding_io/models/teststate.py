import uuid as uuid

from codeschool import models


class TestState(models.TimeStampedModel):
    """
    Register iospec expansions for a given question.
    """

    class Meta:
        unique_together = [('question', 'hash')]

    question = models.ForeignKey('CodingIoQuestion')
    hash = models.models.CharField(max_length=32)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    pre_tests_source = models.TextField(blank=True)
    post_tests_source = models.TextField(blank=True)
    pre_tests_source_expansion = models.TextField(blank=True)
    post_tests_source_expansion = models.TextField(blank=True)

    @property
    def is_current(self):
        return self.hash == self.question.test_state_hash

    def __str__(self):
        status = 'current' if self.is_current else 'outdated'
        return 'TestState for %s (%s)' % (self.question, status)
