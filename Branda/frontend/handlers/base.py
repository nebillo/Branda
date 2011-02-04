"""
.. module:: Base Handler
   :platform: Tornado Web Framework
   :synopsis: Base Handler

.. moduleauthor:: Branda Developing Team <dev@branda.something>

"""

import datetime
import tornado.web
from tornado.options import options

from config.config import *
from model.user import *
from libs.facebook import *


class BaseHandler(tornado.web.RequestHandler):
    
    def get_facebook_cookie(self):
        
        """Check facebook cookie.

        :param name: self.
        :type name: delf.
        :param state: Current state to be in.
        :type state: bool.
        :returns:  cookie or None.
        :raises: Nothing

        """
        cookies = dict((n, self.cookies[n].value) for n in self.cookies.keys())
        cookie = get_user_from_cookie(
            cookies, options.facebook_app_id, options.facebook_app_secret)
        return cookie
    
    def get_current_user(self):
        
        """Validate the facebook cookie and get user info from db.

        :param name: self.
        :type name: self.
        :param state: Current state to be in.
        :type state: bool.
        :returns:  Instanced User Object or None.
        :raises: Nothing

        """
        
        fb_cookie = self.get_facebook_cookie()
        if not fb_cookie:
            self.clear_cookie("user")
            return None
        
        # validate cookie
        fb_uid = fb_cookie["uid"]
        user_cookie = self.get_secure_cookie("user")
        if fb_uid != user_cookie:
            return None
        
        # read user from db with fb_uid
        query = User.all()
        query.filter('facebook_id =', fb_uid)
        user = query.get()
        return user