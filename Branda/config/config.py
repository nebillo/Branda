import os


if os.environ['SERVER_SOFTWARE'].startswith('Dev'):
    # development
    from config_dev import *
else:
    # production
    from config_prod import *
