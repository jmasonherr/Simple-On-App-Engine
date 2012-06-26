import markdown
from google.appengine.ext import blobstore
from google.appengine.ext import db

class Post(db.Model):
    title = db.StringProperty()    
    slug  = db.StringProperty() # Must make this unique
    text  = db.TextProperty(default = '')
    htmltext  = db.TextProperty(default = '')    # stores html of markdown text
    draft = db.BooleanProperty(default=True)
    views = db.IntegerProperty(default=0)
    created_at = db.DateProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty()

    def delete(self):
        for photo in self.photos:
            photo.blob.delete()
            photo.delete()
        super(Post, self).delete()
        
    def render_content(self):
        self.htmltext = markdown.Markdown(extensions=['fenced_code'], output_format="html5", safe_mode=True).convert(self.text)
        #self.htmltext = markdown2.Markdown(safe_mode=True).convert(self.text)


class Photo(db.Model):
    image_url = db.StringProperty()
    blob = blobstore.BlobReferenceProperty()
    post = db.ReferenceProperty(Post, collection_name='photos')
