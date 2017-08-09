#
# List of all installed apps
INSTALLED_APPS = [
    # Extra content
    'codeschool.extra.fresh_install.apps.FreshInstallConfig',

    # Codeschool questions
    'codeschool.questions.code.apps.CodeQuestionConfig',
    'codeschool.questions.numeric.apps.NumericQuestionConfig',
    'codeschool.questions.coding_io.apps.CodingIoQuestionConfig',
    'codeschool.questions.text.apps.TextQuestionConfig',
    'codeschool.questions.free_form.apps.FreeFormQuestionConfig',
    'codeschool.questions.base.apps.QuestionsConfig',

    # Required LMS/Content apps
    'codeschool.lms.activities.apps.ActivitiesConfig',
    'codeschool.lms.attendance.apps.AttendanceConfig',
    'codeschool.lms.activity_lists.apps.ActivityListsConfig',
    'codeschool.lms.classrooms.apps.ClassroomsConfig',
    'codeschool.lms.organizations.apps.OrganizationsConfig',

    # Gamification platform
    # 'codeschool.gamification.points',

    # Optional social apps
    # 'codeschool.social.feed',
    # 'codeschool.social.friends',
    # 'codeschool.questions.text',

    # Core apps
    'codeschool.core.users.apps.UsersConfig',
    'codeschool.core.config.apps.ConfigConfig',
    'codeschool.core.files.apps.FilesConfig',
    'codeschool.core.services.apps.ServicesConfig',

    # Related apps
    'model_reference',
    'bricks.app',

    # Wagtail and dependencies
    'codeschool.vendor.wagtailmarkdown',
    'wagtail.contrib.wagtailroutablepage',
    'wagtail.contrib.settings',
    'wagtail.contrib.modeladmin',
    'wagtail.contrib.table_block',
    'wagtail.wagtailforms',
    'wagtail.wagtailredirects',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsites',
    'wagtail.wagtailusers',
    'wagtail.wagtailsnippets',
    'wagtail.wagtaildocs',
    'wagtail.wagtailimages',
    'wagtail.wagtailsearch',
    'wagtail.wagtailadmin',
    'wagtail.wagtailcore',
    'modelcluster',
    'taggit',

    # Userena
    'guardian',
    'easy_thumbnails',

    # Other 3rd party
    'friendship',
    'polymorphic',
    'django_extensions',
    'rest_framework',
    'rules',

    # Wagtail admin requires this even in production. We simply disable the
    # staticfiles urls in production
    'django.contrib.staticfiles',

    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',

    # OAuth Social Authentication 
    'social_django',
]
#
