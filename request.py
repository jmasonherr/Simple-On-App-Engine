import webapp2
import os
from google.appengine.api import users

from google.appengine.ext.webapp import template

 
TEMPLATE_SUBDIR = 'templates'




class CRequestHandler(webapp2.RequestHandler):
    def get_template(self, template_name):
        return os.path.join(os.path.dirname(__file__), 
                            TEMPLATE_SUBDIR,
                            template_name)

    def render_template(self, template_name, template_vars):
		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'
		base_template_vars = {
                        'application_name': 'BIGGERFASTERMORE', 
                        'users': users, 
                        'user' : users.GetCurrentUser(), 
                        'is_admin':users.is_current_user_admin(),
                        'url':url, 
                        'url_linktext': url_linktext,
                        'ANALYTICS_ID': 'UA-30587223-1',
                        'GITHUB_USERNAME': 'jmasonherr',
                        'CONTACT_EMAIL': 'jmasonherr@gmail.com',
                        'BLOG_TITLE' : 'BIGGERFASTERMORE',
                        'TWITTER':'',
                        'BLOG_TAGLINE' : 'Bringing you more bigger, faster',
                        'BLOG_URL' : 'http//:www.biggerfastermore.com',
                        }
		template_vars.update(base_template_vars)
		template_path = self.get_template(template_name)
		return template.render(template_path, template_vars)

