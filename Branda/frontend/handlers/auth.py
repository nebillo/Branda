from base import *


class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html", options = options, title = "Login")

class AuthHandler(BaseHandler):
    def get(self):
        fb_cookie = self.get_facebook_cookie()
        if not fb_cookie:
            raise tornado.web.HTTPError(401)
        
        # save user token
        fb_uid = fb_cookie["uid"]
        fb_access_token = fb_cookie["access_token"]
        self.set_secure_cookie("user", fb_uid)
        
        # read user from db with fb_uid
        query = BAUser.all()
        query.filter('facebook_id =', fb_uid)
        user = query.get()  
        if not user:
            # create new user with fb_uid
            user = BAUser(facebook_id = fb_uid, facebook_access_token = fb_access_token, created_at = datetime.datetime.now())
        else:
            # update access token
            user.facebook_access_token = fb_access_token
        user.put()
        
        if self.get_argument("redirect", False):
            self.redirect(self.application.settings['post_login_url'])
        else:
            string = "facebook user: " + fb_uid + "<br>connected to branda user: " + str(user.key())
            self.write(string)