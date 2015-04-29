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
        response_data = Tools.getParsedXML(toDefine, WP)
        self.render("definition.html", **{"master":response_data})
