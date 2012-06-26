import os, sys, re, time, datetime
import markdown2
from unicodedata import normalize
from google.appengine.api import users
import webapp2
from request import CRequestHandler
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

from models import *


POSTS_PER_PAGE = 5

def representsInt(d):
    try:
        int(d)
        return True
    except:
        return False

class HomeHandler(CRequestHandler):
    def get(self, page=''):
        q = Post.all().filter('draft =', False).order("created_at")
        posts = []
        more_entries = True
        prev_page = 1
        next_page = 2
        if page and representsInt(page):
            if int(page) > 1:
                prev_page = int(page) -1
            next_page = int(page) + 1
            posts = q.fetch(5, offset=(int(page) - 1) * 5)
        else:
            posts = q.fetch(5)
            
        if len(posts) < 5:
            more_entries = False
            next_page = next_page - 1
        
        self.response.out.write(self.render_template("index.html",{'posts':posts, 'now':datetime.datetime.now(),'next_page':next_page, 'prev_page':prev_page, 'more_entries':more_entries}))


class PostViewHandler(CRequestHandler):
    def get(self, id):
        try:
            post = Post.get_by_id(int(id))
            # not sure if a list is returned here
            post.views = post.views + 1
            post.put()
        except Exception:
            self.redirect('/')
        self.response.out.write(self.render_template("view.html",{'post':post}))


class PostViewSlugHandler(CRequestHandler):
    def get(self, id):
        try:
            post = db.Query(Post).filter('slug =', id.strip()).fetch(1)[0]
            post.views = post.views + 1
            post.put()
            self.response.out.write(self.render_template("view.html",{'post':post, 'pid':post.key().id()}))

        except Exception:
            self.redirect('/')



class FeedHandler(CRequestHandler):
    def get(self):
        
        feed = '''<?xml version="1.0" encoding="UTF-8"?>
                    <rss version="2.0">
                        <channel>
                        <title>BIGGERFASTERMORE</title>
                        <description>Bringing you more bigger, faster</description>
                        <link>http://www.biggerfastermore.com</link>      '''
        for post in Post.all().filter('draft =', False).order("created_at").fetch(15):
                  feed = feed +  ''' <item> 
                                        <title>%s</title>
                                        <description>%s</description> 
                                        <pubDate>%s</pubDate> 
                                        <link>%s</link>  
                                        <guid>%s</guid>  
                                    </item>''' %(post.title, post.htmltext, post.created_ad, 'http://www.biggerfastermore.com/' + post.slug, 'http://www.biggerfastermore.com/' + str(post.key().id()))
                
        feed = feed + "</channel></rss>"
        self.response.headers.add_header('content-type', 'application/rss+xml', charset='utf-8')
        #return Response(generate_feed(), mimetype="application/rss+xml")
        self.response.out.write(feed)

class TestPageHandler(CRequestHandler):
    def get(self):
        self.response.out.write(self.render_template('testpage.html', {}))

application = webapp2.WSGIApplication([
                                ("/testpage", TestPageHandler),
                                ("/preview/(\d+)", PostViewHandler),
                                ("/(\d+)/*", PostViewHandler),
                                ('/page/(\d+)', HomeHandler),
                                ('/page/*', HomeHandler),
                                ("/(\w+)/*", PostViewSlugHandler),
                                ("/feed.rss", FeedHandler),
                                ('/.*', HomeHandler),

],
                              debug=True)


