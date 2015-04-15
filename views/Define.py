"""
Define.py

View that handles the Ajax calls to websters
Dictionary API
"""

from ViewHandler import Handler
from XMLProcessors import WebsterParser as WP
import Tools

       
class DefineHandler(Handler):
    """Handles server side calls to The Dictionary"""
    
    def get(self):
        """Delivers a json object containing the dictionary information for a word"""    
        toDefine = self.request.get("input_str").lower().strip()
        xml = Tools.getXML(toDefine)
        response_data = []
        if xml:
            response_data = [defs.data for defs in WP(xml)]
        self.render("definition.html", **{"master":response_data})