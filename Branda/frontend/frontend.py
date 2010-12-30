# 
# frontend application
#

#from google.appengine.ext import webapp
#from google.appengine.ext.webapp import util
import wsgiref.handlers
import tornado.web
import tornado.wsgi
import os.path

from config.config import *
from frontend.handlers.main import MainHandler
from frontend.handlers.auth import AuthHandler, LoginHandler, LogoutHandler
from frontend.handlers.graph import GraphHandler

       
def main():
    settings = {
        "debug": True,
        "login_url": "/login",
        "post_login_url": "/graph",
        "xsrf_cookies": True,
        "cookie_secret": "32oETzXXAAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    }
    application = tornado.wsgi.WSGIApplication([
        (r"/", MainHandler),
        (r"/login.*", LoginHandler),
        (r"/logout.*", LogoutHandler),
        (r"/auth.*", AuthHandler),
        (r"/graph.*", GraphHandler),
    ], **settings)
    
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()
