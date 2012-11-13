
import re, datetime
from request import CRequestHandler
from models import *
from unicodedata import normalize
import webapp2, json
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images


_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', unicode(word)).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))
    
def representsInt(d):
    try:
        int(d)
        return True
    except:
        return False

class NewPostHandler(CRequestHandler):

    def handleThis(self, title):
        post = Post()
        post.title = title
        post.slug = slugify(post.title)
        post.updated_at = datetime.datetime.now()
        post.put()
        return post
    def post(self):
        title = self.request.get('title')
        post = self.handleThis(title)
        self.redirect("/admin/edit/" +  str(post.key().id()))
    def get(self):
        title = self.request.get('title')
        post = self.handleThis(title)
        self.redirect("/admin/edit/" +  str(post.key().id()))



class EditPostHandler(CRequestHandler):
    def get(self, id):
        post = Post.get_by_id(int(id))
        upload_url = blobstore.create_upload_url('/admin/photo/upload')
        self.response.out.write(self.render_template("edit.html", {'post':post, 'upload_url':upload_url}))
        
    def post(self, id):
        #try:
        bpost = Post.get_by_id(int(id))
        #except Exception:
        #    print 'error'
        #    return
        bpost.title = self.request.get("post_title")
        bpost.text  = self.request.get("post_content")
        bpost.slug = slugify(bpost.title)
        bpost.updated_at = datetime.datetime.now()
        if u'1' in self.request.get_all("post_draft"):
            bpost.draft = True
        else:
            bpost.draft = False
        bpost.render_content()
        for pic in bpost.photos:
            if pic.key().name() not in bpost.text:
                pic.blob.delete()
                pic.delete()
        bpost.put()
        self.redirect("/admin/edit/" + str(bpost.key().id()))


class DeletePostHandler(CRequestHandler):
    def get(self, id):
        self.doThis(id)
    def post(self, id):
        self.doThis(id)
        
    def doThis(self, id):
        #try:
        post = Post.get_by_id(int(id))
        #except Exception:
        #    print 'error'
        #    return
        post.delete()
        self.redirect('/admin/')

class AdminHandler(CRequestHandler):

    def get(self):
        self.handleThis()

        
    def handleThis(self):
        drafts = Post.all().filter('draft =', True).order('created_at').fetch(50)
        posts  = Post.all().filter('draft =', False).order('created_at').fetch(50)
        self.response.out.write(self.render_template("admin.html", {'drafts':drafts, 'posts':posts}))

    
    def post(self,id):
        #try:
        post = Post.get_by_id(int(id))
        #except Exception:
        #    print 'error'
        #return
        post.title = self.request.get("title")
        post.slug = slugify(post.title)
        post.text = request.form.get("content")
        post.render_content()
        post.updated_at = datetime.datetime.now()
        post.put()
        self.response.out.write(self.render_template("admin.html", {'drafts':drafts, 'posts':posts}))
    

class PreviewHandler(CRequestHandler):

    def get(self,id):
        try:
            drafts = db.Query(Post).order('-created_at').fetch(50)
        except Exception:
            print 'error'
            return
        self.response.out.write(self.render_template("post_preview.html", {'post':post}))

class ImageDeleteHandler(CRequestHandler):  # deletes an image and all 
    def get(self,id):
        alter_pic = db.get(id)
        item = alter_pic.item
        alter_pic.blob.delete()
        alter_pic.delete()
        self.redirect('/item/%s' % item.key().name())
        
class ItemDeleteHandler(CRequestHandler):  # deletes an image and all 
    def get(self,id):
        item = BCItem.get_by_key_name(id)
        for photo in item.photos:
            photo.blob.delete()
            photo.delete()
        item.delete()
        self.redirect('/')

 

class UploadURLHandler(CRequestHandler):  
    def get(self):
        upload_url = blobstore.create_upload_url('/admin/photo/upload')
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(upload_url)
    def post(self):
        upload_url = blobstore.create_upload_url('/admin/photo/upload')
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(upload_url)
 
class PhotoUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        # 'file' is file upload field in the form
        blob_info = self.get_uploads('file')[0]
        #self.redirect('/admin/photo/upload/?bkey=%s&pageid=%s' % (blob_info.key(),self.request.get('pageid')))

    #def get(self):
        pageid = self.request.get('pageid')
        #blob = self.request.get('bkey')
        blob = blob_info.key()
        blogpost = Post.get_by_id(int(pageid))

        image_url = images.get_serving_url(blob)
        image = Photo.get_or_insert(image_url)
        image.post = blogpost
        image.blob = blob 
        blogpost.put()
        image.put()

        #self.response.headers['Content-Type'] = 'text/plain'
        my_response = [{'text':'![Alt text](%s "Optional title")' % image.key().name(), 'uploadUrl':blobstore.create_upload_url('/admin/photo/upload')}]
        my_json = json.dumps(my_response)
        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        self.response.out.write(my_json)
        #self.response.out.write('![Alt text](%s "Optional title")' % image.key().name())


application = webapp2.WSGIApplication([
                                ("/admin/photo/upload.*", PhotoUploadHandler),
                                ("/admin/new*", NewPostHandler),
                                ("/admin/preview/(\d+)/*", PreviewHandler),
                                ("/admin/save/(\d+)/*", AdminHandler),
                                ("/admin/edit/(\d+)/*", EditPostHandler),
                                ("/admin/delete/(d+)/*", DeletePostHandler),
                                (".*", AdminHandler),


],
                              debug=True)