from google.appengine.ext import db

class Word(db.Model):
    """Simple Word Model"""
    word_str = db.StringProperty(required=True)
    in_scrabble = db.BooleanProperty()
    in_wwf = db.BooleanProperty()