#Tools.py
import webapp2
import jinja2
import os
import datetime
import logging as logger
import urllib2
from hidden import _dictionaryAPIKey, _dictionaryAPIAddress
from google.appengine.ext import db

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ['DJANGO_SETTINGS_MODULE'] = "myproject.settings"

#directories
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
static_dir = os.path.join(os.path.dirname(__file__), 'static')
media_dir = os.path.join(os.path.dirname(__file__), 'media')

#jinja
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)
    
#MajorRelease.StoriesDelivered.HotfixesDelievered
version = "5.0.2";
    
def getXML(toDefine):
    """Return an XML tree with all of the information of a word from Websters or None"""
    #get definition in xml format
    req = urllib2.Request(_dictionaryAPIAddress.format(word=toDefine, key=_dictionaryAPIKey))
    req.add_header('User-agent', 'isThatAWord.net')
    xml = None
    try:
        xml = urllib2.urlopen(req).read()
    except URLError:
        return
    #reads the xml into a string and then return an XML tree from that string
    return ET.fromstring(xml)     

#Checks if version is up to date and updates it if it is not
#This is used to reset the local storage on the client side
def isUpToDate(handler):
    correctVersion = version == handler.request.cookies.get("version","")
    if not correctVersion:
        handler.response.headers.add_header("Set-Cookie", 'version=%s Expires=%s'%(version,get_expiration()))
    
    return correctVersion
    
def get_expiration(howManyYears=1):
    max_age = howManyYears*365*24*60*60
    return datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S EST")
    
        
def wordExists(word_str):
    """
Run a query checking for the word in our database
and return True if the word is found and False if it
isn't found.
    """
    query = db.GqlQuery("SELECT * FROM Word WHERE word_str = '%s' LIMIT 1"%word_str).get()
    exists = query != None
    if exists:
        word_id = query.key().id()
    else:
        word_id = -1
    return exists, word_id
        