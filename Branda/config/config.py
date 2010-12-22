import os


if os.environ['SERVER_SOFTWARE'].startswith('Dev'):
    # development
    from config_dev import *
else:
    # production
    from config_prod import *

define("facebook_permissions", help="facebook permissions",
       default="email,offline_access,user_birthday,user_religion_politics,user_location")