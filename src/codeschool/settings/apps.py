#
# List of all installed apps
#
INSTALLED_APPS = [
    # Codeschool optional apps
    'codeschool.questions.code',
    # 'codeschool.questions.free_form',
    'codeschool.questions.numeric',
    'codeschool.questions.coding_io',
    # 'codeschool.lms.attendance',
    # 'codeschool.lms.classrooms',
    # 'codeschool.lms.academic',
    # 'codeschool.gamification.points',
    # 'codeschool.social.feed',
    # 'codeschool.social.friends',
    # 'codeschool.questions.text',
    # 'codeschool.cli',

    # Extra content
    'codeschool.extra.fresh_install',

    # Required LMS/Content apps
    'codeschool.questions',
    'codeschool.lms.activities',

    # Core apps
    'codeschool.core.users.apps.UsersConfig',
    'codeschool.core.config.apps.ServerConfigConfig',
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
    # 'userena',
    'guardian',
    'easy_thumbnails',

    # Other 3rd party
    'friendship',
    'polymorphic',
    'django_extensions',
    'rest_framework',
    'rules',

    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',

    # Wagtail admin requires this even in production. We simply disable the
    # staticfiles urls in production
    'django.contrib.staticfiles',
]



