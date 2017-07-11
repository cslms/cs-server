import os

DEBUG = os.environ.get('DEBUG', 'false') == 'true'

from ._paths import *  # noqa
from ._codeschool import *  # noqa
from ._apps import INSTALLED_APPS  # noqa
from ._secrets import SECRET_KEY # noqa
from ._config import * # noqa
from ._logging import LOGGING  # noqa
from ._templates import TEMPLATES  # noqa
