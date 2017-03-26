# -*- coding: utf8 -*-
#
# This file were created by Python Boilerplate. Use boilerplate to start simple
# usable and best-practices compliant Python projects.
#
# Learn more about it at: http://github.com/fabiommendes/boilerplate/
#

import os
from setuptools import setup, find_packages


# Meta information
version = open('VERSION').read().strip()
dirname = os.path.dirname(__file__)


# Save version and author to __meta__.py
base = os.path.join(dirname, 'src', 'codeschool')
data = '''# Automatically created. Please do not edit.
__version__ = u'%s'
__author__ = u'F\\xe1bio Mac\\xeado Mendes'
''' % version
if os.path.exists(base):
    path = os.path.join(base, '__meta__.py')
    with open(path, 'wb') as F:
        F.write(data.encode())

# Obtain long description from README.rst
if os.path.exists('README.rst'):
    long_description = open('README.rst').read()
else:
    long_description = ''


setup(
    # Basic info
    name='codeschool',
    version=version,
    author='Fábio Macêdo Mendes',
    author_email='fabiomacedomendes@gmail.com',
    url='',
    description='An environment for teaching programming for 21st century '
                'students.',
    long_description=long_description,

    # Classifiers (see https://pypi.python.org/pypi?%3Aaction=list_classifiers)
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],

    # Packages and depencies
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        # Non-django dependencies
        'lazyutils>=0.3.1',
        'pygeneric',
        'mistune',
        'pygments',
        'Markdown',
        'html5lib',
        'bleach',
        'fake-factory',
        'factory-boy',
        'mommys_boy',
        'celery[redis]',
        'PyYAML',
        'json-rpc',

        # Services
        'invoke',

        # Django and extensions
        'django==1.10',
        'django-polymorphic',
        'django-model-utils',
        'django-model-reference',
        'django-picklefield',
        'django-jsonfield',
        'django-userena', 'django-guardian>=1.4.6',
        'django-ipware',
        'django-annoying',
        'django-extensions',
        'django-redis',
        'social-auth-app-django',
        'django-compressor',
        'django-extensions',
        'djangorestframework',
        'werkzeug',

        # Wagtail
        'wagtail',
        'wagtail-model-tools>=0.1.4',

        # Jinja support
        'jinja2<2.9',

        # CodingIo question libraries
        'markio>=0.2.6',
        'iospec>=0.3.16',
        'ejudge>=0.5.17',
        'boxed>=0.3.11',

        # Related libraries
        'srvice>=0.1.5',
    ],
    extras_require={
        'dev': [
            'ipython',
            'manuel',
            'mock',
            'python-boilerplate',
            'invoke',
            'pytest',
            'flake8',
            'tox',
            'pytest-cov',
            'pytest-django',
            'pytest-selenium',
            'pytest-factoryboy',
            'sulfur>=0.1.3',
        ]
    },

    # Other configurations
    zip_safe=False,
    platforms='any',
)
