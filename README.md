### Super easy clean and simple. Svbtle-like blogging on Google App Engine ###

This code is modified from Svbtle, [Simple](https://github.com/orf/simple), and the [jQuery drag and drop image uploader](http://blueimp.github.com/jQuery-File-Upload/)

The code is HTML5, fairly minimal, and very simple.  Posts are written in markdown, and image handling is done by google's image cloud.  Download the repository, make your personalizations, load into App Engine Launcher, deploy and begin blogging.

* Change the following to make it work for you:
+ change all of your info in request.py
+ /static/images/logo.png is where your logo goes
+ change 'biggerfastermore' to your own blog name in app.yaml

All of your admin activites are located at /admin/

### The Best Part ###
Images are hosted using [GAE's image service](https://developers.google.com/appengine/docs/python/images/functions). Super fast, easy, and resizable.  

To **add an image**, just **drag** it on to the page when you're editing a post.   The necessary markdown to display the image will automagically appear at the end of the post

To **delete an image**, remove any mentions of it from the post.  It will automagically be deleted from the server

To **resize an image, add '=sXX' to the end** of the source url
For example, the following image:

### Normal ###
http://lh6.ggpht.com/q4mdXHDOOVQpgm21hUcBrcIHKA_3Mn7OIRyUO63y9KuVhYa9H5cV08a3kJWznB6CII0dqSPGfxhvMe6pCIO884M4uNFoT3g
![Largest](http://lh6.ggpht.com/q4mdXHDOOVQpgm21hUcBrcIHKA_3Mn7OIRyUO63y9KuVhYa9H5cV08a3kJWznB6CII0dqSPGfxhvMe6pCIO884M4uNFoT3g "Normal")

### Medium ###
http://lh6.ggpht.com/q4mdXHDOOVQpgm21hUcBrcIHKA_3Mn7OIRyUO63y9KuVhYa9H5cV08a3kJWznB6CII0dqSPGfxhvMe6pCIO884M4uNFoT3g=**s200**
![Medium](http://lh6.ggpht.com/q4mdXHDOOVQpgm21hUcBrcIHKA_3Mn7OIRyUO63y9KuVhYa9H5cV08a3kJWznB6CII0dqSPGfxhvMe6pCIO884M4uNFoT3g=s200 "medium")

### Small ###
http://lh6.ggpht.com/q4mdXHDOOVQpgm21hUcBrcIHKA_3Mn7OIRyUO63y9KuVhYa9H5cV08a3kJWznB6CII0dqSPGfxhvMe6pCIO884M4uNFoT3g=**s100**
![Small](http://lh6.ggpht.com/q4mdXHDOOVQpgm21hUcBrcIHKA_3Mn7OIRyUO63y9KuVhYa9H5cV08a3kJWznB6CII0dqSPGfxhvMe6pCIO884M4uNFoT3g=s100 "small")

`image from Wikipedia`