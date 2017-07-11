from django.utils.translation import ugettext_lazy as _

from codeschool import models


def feature(name, description='', image=None, icon=None):
    """
    Create a feature method.
    """

    def method(self, commit=True):
        feature = Feature(
            name=name,
            description=description or name,
            image=image,
            icon=icon,
            board=self,
        )
        if commit:
            feature.save()
        return feature

    return method


class SentimentBoard(models.TimeStampedModel):
    """
    Represents sentiments of a group of users towards a group of
    generic features.

    This is usually used to communicate the level of competence of each member
    in the team with different technologies.
    """

    name = models.CodeschoolNameField()
    members = models.ManyToManyField(
        models.User,
        related_name='sentiment_boards',
    )

    # Functions that define common features
    feature_python = feature('Python')
    feature_django = feature('Django')
    feature_elm = feature('Elm')
    feature_html5 = feature('HTML5')
    feature_js = feature('JS', 'Javascript (ES5)')
    feature_js6 = feature('ES6', 'Javascript ES6')
    feature_css = feature('CSS')

    # ... and the list goes on. Contribute!


class Feature(models.Model):
    """
    A Feature in a sentiment board.
    """

    board = models.ParentalKey(SentimentBoard, related_name='features')
    name = models.CodeschoolNameField()
    description = models.CodeschoolDescriptionField(blank=True)
    image = models.ImageField(blank=True, null=True)
    icon = models.CharField(max_length=50)

    class Meta:
        unique_together = [('board', 'name')]


class Sentiment(models.TimeStampedModel):
    """
    Represents the sentiment of a user towards a feature in a given instant
    of time.
    """

    STATUS_VERY_HAPPY, STATUS_HAPPY, STATUS_NEUTRAL, STATUS_SAD = range(4)
    STATUS_CHOICES = [
        (STATUS_VERY_HAPPY, _('Very happy')),
        (STATUS_HAPPY, _('Happy')),
        (STATUS_NEUTRAL, _('Neutral')),
        (STATUS_SAD, _('Sad')),
    ]

    status = models.SmallIntegerField(
        _('status'),
        choices=STATUS_CHOICES,
    )
    user = models.ForeignKey(
        models.User,
        related_name='sentiments'
    )
    feature = models.ForeignKey(
        Feature,
        related_name='sentiments',
    )
    board = models.ForeignKey(
        SentimentBoard,
        related_name='sentiments',
    )
