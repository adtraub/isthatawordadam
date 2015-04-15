"""
Lookup.py

View that handles the ajax calls for
looking up a word in the site's database
"""
import json
import Tools
from ViewHandler import Handler
            
class LookupHandler(Handler):
    """Checks local dictionary for word"""
    def get(self):
        response_data = {"found":False}        
        input_str = self.request.get("input_str")
        if len(input_str) > 0:#Lookup the word!
            exists,word_id = Tools.wordExists(input_str)
            if exists:
                response_data["found"] = True
                response_data["word_id"] = word_id
        
        self.write(json.dumps(response_data))
                
