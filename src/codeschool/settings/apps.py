#
# List of all installed apps
#

INSTALLED_APPS = [
    # Codeschool optional apps
    'codeschool.questions.code',
    'codeschool.questions.free_form',
    'codeschool.questions.numeric',
    'codeschool.questions.coding_io',
    'codeschool.lms.attendance',
    'codeschool.lms.classrooms',
    'codeschool.lms.academic',
    # 'codeschool.gamification',
    # 'codeschool.social.feed',
    # 'codeschool.social.friends',
    'codeschool.cli',

    # These are always required
    'codeschool.questions',
    'codeschool.lms.activities',
    'codeschool.accounts',
    'codeschool.core',

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
    'userena',
    'easy_thumbnails',
    'guardian',

    # Other 3rd party
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