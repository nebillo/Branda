"""
.. module:: Auth Handler
   :platform: Tornado Web Framework
   :synopsis: Auth Handler

.. moduleauthor:: Branda Developing Team <dev@branda.something>
"""

from base import *


class LoginHandler(BaseHandler):
    def get(self):
      
        """Get Method : Renders login.html page.
        """
        self.render("login.html", options = options, title = "Login")

class LogoutHandler(BaseHandler):
  
    def get(self):
      
        """User Logout. Clear all cookies and redirect to root.

        :param name: self.
        :type name: self.
        """
        self.clear_all_cookies()
        self.redirect("/")

class AuthHandler(BaseHandler):
    def get(self):
      
        """Check if the facebook cookie is in and connect user with facebook login. if not raise error 401. 

        :param name: self.
        :type name: self.
        :param state: Current state to be in.
        :type state: bool.
        :returns: Void
        :raises: tornado.web.HTTPError(401)

        """
        fb_cookie = self.get_facebook_cookie()
        if not fb_cookie:
            raise tornado.web.HTTPError(401)
        
        # save user token
        fb_uid = fb_cookie["uid"]
        fb_access_token = fb_cookie["access_token"]
        self.set_secure_cookie("user", fb_uid)
        
        # read user from db with fb_uid
        query = User.all()
        query.filter('facebook_id =', fb_uid)
        user = query.get()  
        if not user:
            # create new user with fb_uid
            user = User(facebook_id = fb_uid, facebook_access_token = fb_access_token)
        else:
            # update access token
            user.facebook_access_token = fb_access_token
        user.put()
        
        if self.get_argument("redirect", False):
            self.redirect(self.application.settings['post_login_url'])
        else:
            string = "facebook user: " + fb_uid + "<br>connected to branda user: " + str(user.key())
            self.write(string)