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

import jinja2
import webapp2
import os
import logging
#logging.info("DOES THIS WORK?!")

from models.Word import Word

from views.ViewHandler import Handler
from views.Index import IndexHandler, CSSFreeIndexHandler
from views.Direct import DirectLinkHandler, CSSFreeDirectLinkHandler
from views.WordNotFound import WordNotFoundHandler, CSSFreeWordNotFoundHandler
from views.Lookup import LookupHandler
from views.Define import DefineHandler
#from views.Prime import PrimeHandler #adds a value to the datastore to "prime it for local use


app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/nocss', CSSFreeIndexHandler),
    ('/findword', LookupHandler),
    ('/define', DefineHandler),
    ('/direct/([0-9]+)',DirectLinkHandler),
    ('/nocss/direct/([0-9]+)',CSSFreeDirectLinkHandler),
    ('/wordnotfound',WordNotFoundHandler),
    ('/nocss/wordnotfound',CSSFreeWordNotFoundHandler),
    #('/primedatastore',PrimeHandler),
], debug=True)