#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os, cgi
import webapp2

import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t=jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
    def renderError(self, error_code):
        self.error(error_code)
        self.response.write("Hey! Don't do that!")
class Blog(db.Model):
    title = db.StringProperty(required = True)
    body = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_mod = db.DateTimeProperty(auto_now = True)
class ViewPostHandler(webapp2.RequestHandler):

    def get(self, id="" ):
        # body = self.request.get("body")
        blog = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC")
        # # num = Blog.key(bi).id()
        t = jinja_env.get_template("blog.html")
        # id = Blog.get_by_id(blog)
        content = t.render(id=id)
        # last = Blog.get_by_id(key().id())
        # db.GqlQuery("SELECT * FROM Blog ORDER BY last_mod")

        self.response.write(content)
class ViewPost(Handler):
    def render_base(self, title="", body="", error=""):
        blog = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC LIMIT 5")
        self.render("blog.html", title=title, blog = blog, error=error)

    def get(self):
        self.render_base()

  # permalink
class NewPost(Handler):
    def renderform(self, title= "", body="", error=""):
        # t = jinja_env.get_template("newpost.html")
        # content = t.render(title=title, body=body, error=error)
        self.render("newpost.html", title=title, body=body, error=error)
    def get(self):
        """Display post page as seen in login in flicklist"""
        self.renderform()

    def post(self):
        title = self.request.get("title")
        body = self.request.get("body")
        link =self.request.get("last_mod")

        if title and body:
            b = Blog(title = title, body = body)
            b.put()
            self.redirect("/blog")
        else:
            error = "Need title and body"
            self.renderform(title, body, error)

class Base(Handler):
    def render_base(self, title="", body="", error=""):
        blog = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC LIMIT 5")
        self.render("base.html", title=title, blog = blog, error=error)

    def get(self):
        self.render_base()
    def post(self):
        title = self.request.get("title")
        body = self.request.get("body")

        if title and body:
            b = Blog(title = title, body = body)
            b.put()
            self.redirect("/blog")
        else:
            error = "Need title and body"
            self.render_base(title, body, error)

app = webapp2.WSGIApplication([
    # ('/', PostHandler),
    ('/', Base),
    ('/blog', ViewPost),
    ('/newpost', NewPost),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler)
], debug=True)
