import pandas as pd
from django.utils.translation import ugettext_lazy as _

from codeschool import models
from codeschool.lms.activity_lists.validators import material_icon_validator
from .managers import ActivityListManager
from .score_map import ScoreMap


class ActivityList(models.TimeStampedModel):
    """
    List of activities.
    """

    name = models.CodeschoolNameField()
    slug = models.CodeschoolSlugField()
    short_description = models.CodeschoolShortDescriptionField()
    long_description = models.CodeschoolDescriptionField()
    icon = models.CharField(
        _('Optional icon'),
        max_length=20,
        default='code',
        validators=[material_icon_validator],
        help_text=_(
            'Name of the material design icon. Check full list at: '
            'https://material.io/icons'
        ),
    )

    class Meta:
        verbose_name = _('List of activities')
        verbose_name_plural = _('Lists of activities')

    objects = ActivityListManager()

    def score_board_total(self) -> ScoreMap:
        """
        Return a score board mapping with the total score for each user.
        """

        board = self.score_board()
        scores = ScoreMap(self.title)
        for k, L in board.items():
            scores[k] = sum(L)
        return scores

    def grades_as_csv(self) -> str:
        """
        Return a string with CSV data for the all student submissions inside
        the given section.
        """

        return self.grades_as_dataframe().to_csv()

    def grades_as_dataframe(self) -> pd.DataFrame:
        """
        Return a Pandas dataframe with the grades for all students that
        submited responses to questions in the given list.
        """

        from codeschool.lms.activities.models import Progress

        children = self.get_children()
        children_id = children.values_list('id', flat=True)
        cols = ('user__username', 'user__email',
                'user__first_name', 'user__last_name',
                'activity_page__title', 'given_grade_pc')
        responses = (
            Progress.objects
                .filter(activity_page__in=children_id)
                .values_list(*cols)
        )
        responses = list(responses)

        # User data
        users_data = sorted({row[0:4] for row in responses})
        users = pd.DataFrame(
            users_data,
            columns=['username', 'email', 'first_name', 'last_name'],
        )
        users.index = users.pop('username')

        # Question data
        df = pd.DataFrame(responses, columns=cols)
        groups = df.groupby('activity_page__title')
        by_question = {
            name: group[['user__username', 'given_grade_pc']]
            for name, group in groups}

        # Agregate question data
        result = users.copy()
        for name, df in by_question.items():
            col = df['given_grade_pc']
            col.index = df['user__username']
            result[name] = col

        return result
