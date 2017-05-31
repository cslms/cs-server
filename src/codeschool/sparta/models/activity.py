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

    def populate_from_csv(self, csv_data):
        """
        Parse CSV data and populate the user grades.
        
        Args:
            csv_data (str): 
                A CSV file with two columns. The first column must be username
                and the second column is a grade in [0..100]
        """

        csv_file = io.StringIO(csv_data)
        reader = csv.reader(csv_file, delimiter=';', quotechar='"')
        for row in reader:
            user_name = row[0]
            if not self.user_grade:
                user = models.User.objects.get(username=user_name)
                self.user_grade = UserGrade()
                self.user_grade.user = user

            self.user_grade.grade = row[1]
            self.user_grade.save()


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
    csv_file = io.StringIO(csv_data)
    reader = csv.reader(csv_file, delimiter=';', quotechar='"')
    for row in reader:
        if isinstance(row[0], str) and \
           isinstance(row[1], Number) and \
           0 <= row[1] <= 100:
            users_grade.append(row)


class UserGrade(models.Model):
    """
    Represents a user with your grade.
    """
    grade = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    activity = models.ForeignKey(SpartaActivity, related_name='user_grade')
    user = models.ForeignKey(models.User)

    class Meta:
        unique_together = [('activity', 'user')]
