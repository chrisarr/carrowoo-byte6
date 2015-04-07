#!/usr/bin/env python
from jinja2 import TemplateNotFound
import os

import webapp2
from webapp2_extras import jinja2
from webapp2_extras import json
import httplib2
import urllib

# BaseHandler subclasses RequestHandler so that we can use jinja
class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(app=self.app)

        # This will call self.response.write using the specified template and context.
        # The first argument should be a string naming the template file to be used. 
        # The second argument should be a pointer to an array of context variables
        #  that can be used for substitutions within the template
    def render_response(self, _template, context):
        values = {'url_for': self.uri_for}
        #logging.info(context)
        values.update(context)
        self.response.headers['Content-Type'] = 'text/html'

        try:
            # Renders a template and writes the result to the response.
            rv = self.jinja2.render_template(_template, **values)
            self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
            self.response.write(rv)

        except TemplateNotFound:
            self.abort(404)


# Class MainHandler now subclasses BaseHandler instead of webapp2
class MainHandler(BaseHandler):
    # This method should return the html to be displayed
    def get(self):
        variables={}
        # and render the response
        self.render_response('index.html', variables)


app = webapp2.WSGIApplication([('/', MainHandler)], debug=True)