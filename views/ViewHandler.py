"""
ViewHandler.py

Parent class for all views
"""
import Tools
import webapp2


class Handler(webapp2.RequestHandler):
    """Helper class to make handling easier"""    
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        t = Tools.jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))