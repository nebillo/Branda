import os


if os.environ['SERVER_SOFTWARE'].startswith('Dev'):
    # development
    from config_dev import *
else:
    # production
    from config_prod import *

define("facebook_permissions", help="facebook permissions",
       default="user_birthday,user_religion_politics,user_likes,user_checkins,user_events")