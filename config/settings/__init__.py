from os import getenv

from .base import *

if getenv('ENVIRONMENT') == 'PRODUCTION':
    from .production import *
else:
    from .develop import *
