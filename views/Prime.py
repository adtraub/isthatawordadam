"""
test.py

This view is designed to allow me to add a single word to the datastore.

"""
from ViewHandler import Handler
import Tools

class PrimeHandler(Handler):
    """Parent Class for homepage"""
    def get(self): 
        Tools.addSampleData(["test"])
        self.render("prime.html")