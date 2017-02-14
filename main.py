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
import os
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
class Blog(db.Model):
    title = db.StringProperty(required = True)
    body = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
class ViewPostHandler(Handler):
    def get(self): #blog_id):
        # blog=self.request.get("blog_link")
        # blog_link = Blog.get_by_id(int(blog_id))
        # if not blog:
        #     self.renderError(404)

        t = jinja_env.get_template("/newpost.html")
        # content = t.render(blog=blog)
        self.response.write(t)
  # permalink
class NewPost(Handler):
    def get(self):
        self.write()
class MainPage(Handler):
    def render_base(self, title="", body="", error=""):
        blog = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC")
        self.render("base.html", title=title, body=body, error=error, blog=blog)

    def get(self):
        self.render_base()
    def post(self):
        title = self.request.get("title")
        body = self.request.get("body")

        if title and body:
            b = Blog(title = title, body = body)
            b.put()
            self.redirect("/")
        else:
            error = "Need title and body"
            self.render_base(title, body, error)
# class ViewPostHandler(Handler):
#     def get (self, id):
#         self.redirect("/newpost.html")


app = webapp2.WSGIApplication([
    # ('/newpost', PostHandler),
    ('/', MainPage),
    ('/newpost.html', ViewPostHandler),
    webapp2.Route('.blog/<blog_id:\d+>',ViewPostHandler)
], debug=True)
