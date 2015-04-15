"""
Index.py

Class for index views

"""
from ViewHandler import Handler
import Tools

class IndexParent(Handler):
    """Parent Class for homepage"""
    def get(self): 
        self.render('isThatAWord.html', **{"input_str":self.request.get("input_str"), "use_css":self.use_css, "is_up_to_date":Tools.isUpToDate(self),})

class IndexHandler(IndexParent):
    """Handles Main Page"""
    use_css = True
        
class CSSFreeIndexHandler(IndexParent):
    """Handles Main Page without CSS"""
    use_css = False