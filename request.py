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
                        'application_name': 'my info', 
                        'users': users, 
                        'user' : users.GetCurrentUser(), 
                        'is_admin':users.is_current_user_admin(),
                        'url':url, 
                        'url_linktext': url_linktext,
                        'ANALYTICS_ID': '',
                        'GITHUB_USERNAME': '',
                        'CONTACT_EMAIL': '',
                        'BLOG_TITLE' : 'my blog title',
                        'TWITTER':'',
                        'BLOG_TAGLINE' : 'and a great tagline',
                        'BLOG_URL' : 'http://my.blog.url',
                        }
		template_vars.update(base_template_vars)
		template_path = self.get_template(template_name)
		return template.render(template_path, template_vars)

