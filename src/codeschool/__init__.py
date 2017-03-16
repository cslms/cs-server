"""
Overview of codeschool codebase:

Packages

- accounts: user authentication, login and signup (uses userena)
- cli: command line scripts that helps managing codeschool
- components: jinja2/pyml components
- core: a mixed bag of core functionality
- extra: optional codeschool activities
- fixes: monkey-patch 3rd party libs
- gamification: points, badges and stars
- lms: learning management system, control courses, grades, etc
- questions: implement different question types
- settings: django settings
- site: core templates
- social: social network capabilities
- tests: global tests
- vendor: vendorized libs
"""

from .__meta__ import __author__, __version__

# Useful functions
from codeschool.core import get_sys_page, get_wagtail_root, config_options, global_data_store

# Required services: Redis and Celery support
import codeschool.core.services.redis
import codeschool.core.services.celery

