import os

from codeschool.settings import BASE_DIR

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [os.path.join(BASE_DIR, 'site', 'jinja2')],
        'APP_DIRS': True,
        'OPTIONS': {
            'trim_blocks': True,
            'lstrip_blocks': True,
            'environment': 'codeschool.jinja2.environment',
            'extensions': [
                # 'wagtail.wagtailcore.jinja2tags.core',
                # 'wagtail.wagtailadmin.jinja2tags.userbar',
                # 'wagtail.wagtailimages.jinja2tags.images',
                # 'jdj_tags.extensions.DjangoL10n',
                # 'jdj_tags.extensions.DjangoNow',  # not released yet!
                # 'djinga.ext.static',
                # 'djinga.ext.css',
                # 'djinga.ext.js',
                # 'djinga.ext.media',
                # 'djinga.ext.django',
                # 'djinga.ext.csrf_token',
                # 'djinga.ext.url',
                # 'djinga.ext.htmlcompress.HTMLCompress',  # only on deploy
                'compressor.contrib.jinja2ext.CompressorExtension',
                'jinja2.ext.do',
                'jinja2.ext.loopcontrols',
                'jinja2.ext.with_',
                'jinja2.ext.i18n',
                'jinja2.ext.autoescape',
            ],
        },
    },
    # {
    #     'BACKEND': 'djinga.backends.djinga.DjingaTemplates',
    #     'APP_DIRS': True,
    #     'DIRS': [
    #         os.path.join(BASE_DIR, 'site', 'templates'),
    #     ],
    #     'OPTIONS': {
    #         'jj_exts': ('jinja2', 'jinja'),
    #         'dj_exts': ('html', 'htm'),
    #         'i18n_new_style': True,
    #         'autoescape': False,
    #         #'environment': 'codeschool.settings.jinja2.environment',
    #         'extensions': [
    #             # 'codeschool.jinja.ext.DjangoComment',
    #             # 'codeschool.jinja.ext.DjangoLoad',
    #             # 'wagtail.wagtailcore.jinja2tags.core',
    #             # 'wagtail.wagtailadmin.jinja2tags.userbar',
    #             # 'wagtail.wagtailimages.jinja2tags.images',
    #             # 'jdj_tags.extensions.DjangoL10n',
    #             # 'jdj_tags.extensions.DjangoNow',  # not released yet!
    #             'compressor.contrib.jinja2ext.CompressorExtension',
    #             'djinga.ext.static',
    #             'djinga.ext.css',
    #             'djinga.ext.js',
    #             'djinga.ext.media',
    #             'djinga.ext.django',
    #             'djinga.ext.csrf_token',
    #             'djinga.ext.url',
    #             # 'djinga.ext.htmlcompress.HTMLCompress',  # only on deploy
    #             'jinja2.ext.do',
    #             'jinja2.ext.loopcontrols',
    #             'jinja2.ext.with_',
    #             'jinja2.ext.i18n',
    #             'jinja2.ext.autoescape',
    #         ],
    #         'context_processors': [
    #             'social.apps.django_app.context_processors.backends',
    #             'social.apps.django_app.context_processors.login_redirect',
    #             'django.template.context_processors.request',
    #             'django.contrib.auth.context_processors.auth',
    #             'django.template.context_processors.i18n',
    #             'django.template.context_processors.media',
    #             'django.template.context_processors.static',
    #             'django.template.context_processors.tz',
    #             'django.contrib.messages.context_processors.messages',
    #             # 'django.template.context_processors.debug',
    #             # 'wagtail.contrib.settings.context_processors.settings',
    #         ],
    #         'filters': filters.filter_registry,
    #         'globals': filters.globals_registry,
    #     },
    # },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                #'social.apps.django_app.context_processors.backends',
                #'social.apps.django_app.context_processors.login_redirect',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                # 'django.template.context_processors.debug',
                # 'wagtail.contrib.settings.context_processors.settings',
            ]
        },
    },
]
