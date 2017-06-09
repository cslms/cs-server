from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import csv
from codeschool import models
from codeschool.lms.activities.models import Activity
from django.core.validators import MinValueValidator, MaxValueValidator
import io
from numbers import Number


class SpartaActivity(Activity):
    """
    Represents a sparta activity.
    """
    description = models.TextField()

    class Meta:
        verbose_name = _('Sparta Activity')
        verbose_name_plural = _('Sparta Activities')

    def populate_from_csv(self, csv_data, commit=True):
        """
        Populate DB with user grades.

        Args:
            csv_data (str):
                A CSV file with two columns. The first column must be username
                and the second column is a grade in [0..100]
            commit:
                If false, do not save results on the database.
        """

        if self.id is None:
            raise ValueError('SpartaActivity must have an id')

        data = read_csv_file(csv_data)
        names = [name for name, value in data]
        users = User.objects.filter(username__in=names)
        usernames_map = dict(data)
        user_grades = []

        for user in users:
            value = usernames_map[user.username]
            user_grade = UserGrade(user=user, grade=value, activity=self)
            user_grades.append(user_grade)

        if commit:
            return UserGrade.objects.bulk_create(user_grades, batch_size=100)
        else:
            return user_grades

    def create_post_grade_csv(self):
        """
        Create string list with user post_grades.

        Returns:
            String with user post_grades
        """

        lines = str

        for user_grade in self.user_grades.all():
            line_user_grade = user.username
            if user_grade.post_grade == None:
                line_user_grade += (';', user_grade.grade)
            else:
                line_user_grade += (';', user_grade.post_grade)

            lines += line_user_grade
            lines += '\n'

        return lines


class UserGrade(models.Model):
    """
    Represents a user with your grade.
    """
    grade = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    post_grade = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    activity = models.ForeignKey(SpartaActivity, related_name='user_grades')
    user = models.ForeignKey(models.User)

    class Meta:
        unique_together = [('activity', 'user')]


def read_csv_file(csv_data):
    """
    Read a csv file and validate some details.
    Args:
        csv_data (str):
         A CSV file with two columns. The first column must be username
         and the second column is a grade in [0..100]

    Returns: A array contains the name and grade of all users.

    """
    users_grade = []
    names = set()

    csv_file = io.StringIO(csv_data)
    reader = csv.reader(csv_file, delimiter=';', quotechar='"')

    for name, value in reader:
        value = float(value)
        if name in names:
            continue
        value = max(0.0, min(value, 100.0))
        users_grade.append((name, value))
        names.add(name)
    return users_grade
