"""
WordNotFound

File for bad Permalinks
"""
from ViewHandler import Handler

class WordNotFoundParent(Handler):
    """Parent Class for Bad Permalink Page"""
    def get(self):
        self.render("wordNotFound.html", **{"use_css":self.use_css,}) 
        
class WordNotFoundHandler(WordNotFoundParent):
    """Standard Bad Permalink Page"""
    use_css = True
        
class CSSFreeWordNotFoundHandler(WordNotFoundParent):
    """CSS Free Bad Permalink Page"""
    use_css = False