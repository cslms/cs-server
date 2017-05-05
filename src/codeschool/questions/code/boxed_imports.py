"""
Define modules that should be imported/mocked by boxed sandbox.
"""

import sys

sys.modules['django'] = None
sys.modules['django.conf'] = None
