from codeschool import models


class DescriptiveModel(models.TimeStampedModel):
    """
    Base class for many different models.
    """
    name = models.CodeschoolNameField()
    slug = models.CodeschoolSlugField()
    description = models.CodeschoolDescriptionField(blank=True)

    class Meta:
        abstract = True


class Faculty(DescriptiveModel):
    """
    A faculty institution.

    Each faculty may represent an academic department, school unity,
    """


class Course(DescriptiveModel):
    """
    An academic course.
    """

    faculty = models.ForeignKey('Faculty')


class Discipline(DescriptiveModel):
    """
    An academic discipline.
    """

    faculty = models.ForeignKey('Faculty', blank=True)
    code = models.CharField(max_length=50, blank=True)
    since = models.DateField(blank=True, null=True)

    # These were modeled as in https://matriculaweb.unb.br/, which is not
    # particularly good. In the future we want structured data types.
    syllabus = models.RichTextField(blank=True)
    program = models.RichTextField(blank=True)
    bibliography = models.RichTextField(blank=True)
    # requirements = ... will we ever model this?
    #                it can be more complicated than it looks
