import warnings

from .base import *
from .codeschool import *
from .security import SECRET_KEY
from .apps import INSTALLED_APPS
from .logging import LOGGING
from .templates import TEMPLATES

# Override settings with environment variables
if DEBUG:
    _ns = globals()
    for _var, _value in list(_ns.items()):
        if _var.startswith('CODESCHOOL'):
            _ns[_var] = os.environ.get(_var, _value)
