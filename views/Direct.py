"""
Direct.py

Permalink views
"""
from ViewHandler import Handler
from models.Word import Word
import logging
import Tools

class DirectParent(Handler):
    """Parent class for Permalink pages"""
    def get(self, word_id):
        try:
            p = Word.get_by_id(int(word_id))
            if p:
                logging.info(p)
                self.render("direct.html", **{"input_str":p.word_str, "use_css":self.use_css, "word_id":word_id, "is_up_to_date":Tools.isUpToDate(self),})
            else:
                self.redirect(self.error_page)
        except Exception, e:
            #logger.debug(e)
            self.redirect(self.error_page)
            
class DirectLinkHandler(DirectParent):
    """Standard Permalink"""
    use_css = True
    error_page = "/wordnotfound"

class CSSFreeDirectLinkHandler(DirectParent):
    """CSS Free Permalink"""
    use_css = False
    error_page = "/nocss/wordnotfound"