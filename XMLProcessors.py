"""
Dictionary Processor

"""    
from collections import namedtuple
import logging

class WebsterParser():
    """An Object Oriented approach to parsing the xml from the dictionary api"""
    def __init__(self, xml):
        """Creates a generator to iteratively parse the xml"""
        self.definitionGenerator = (c for c in xml.getchildren() if c.find("def") is not None)

    def __iter__(self):
        """This object can be used as an iterator"""
        return self

    def next(self):
        """Get next definition from the internal definition Generator"""
        node = next(self.definitionGenerator) #current def node
        defObject = DefinitionEntry()#Object to hold the definition data for each entry
        self.getSimpleData(defObject, node)#gets the data that can be retrieved fairly easily
        self.buildDefinition(defObject, node.find("def"))#gets any and all definitions for this entry
        self.setupSound(defObject)
        return defObject

    def getSimpleData(self, defObject, node):
        """Gets the non-definition data from the node and stores it in the definition object"""
        for val in ("sound/wav","pr","hw", "et", "fl"):
            current = node.find(val)
            if current is not None:
                defObject.addItem(val, " ".join([t for t in current.itertext()]))
    
    def buildDefinition(self, defObject, defRoot):
        """builds the definition/s for this entry"""
        heading = ""
        subheading = ""
        details = []
        contains_transitive_and_intransitive = len(defRoot.findall("vt")) == 2
            
        
        for node in defRoot:
            #handle the date
            if node.tag == "date":
                defObject.addItem("date",node.text)
            
            #handle the headings and subheadings
            elif node.tag == "sn":
                #if it has any text (not including child tags
                if node.text:
                    #add the previous entry if one exists
                    if details:
                        self.checkForAndRemoveLeadingColon(details, subheading)
                        defObject.data["definitions"].append(DefinitionTuple(heading,subheading, details))
                        heading = "" 
                        subheading = ""
                        details = []
                        

                    #split up the text to check for a heading
                    splitText = node.text.split()
                    
                    #if it has a heading
                    if splitText[0].isdigit():
                        heading = splitText[0]
                        subheading += " ".join(splitText[1:])
                    #no heading
                    else:
                        subheading += " ".join(splitText)
                
                #get the text of the children of the sn element
                for kid in node.getchildren():
                        #usually (1) (2) etc...
                        details.append(HTMLString(" ".join([t for t in kid.itertext()]),"s",))
        
            #italic text in definition
            elif node.tag == "ssl":
                details.append(HTMLString(node.text,"i",))
            
                """
            if I could get top level text, 
            and children text while knowing 
            what text is in what tag, 
            I could do su much more here
                """
            #definition text 
            elif node.tag == "dt":
                details.append(HTMLString(" ".join([t for t in node.itertext()])))
            
            #If the definition contains trans and intrans
            elif node.tag == "vt" and contains_transitive_and_intransitive:
                details.append(HTMLString(node.text, "vt"))
                
            #Update part of speech to trans or intrans depending on type
            elif node.tag == "vt":
                defObject.addItem("fl",node.text)
                
                
        self.checkForAndRemoveLeadingColon(details, subheading)
        defObject.data["definitions"].append(DefinitionTuple(heading,subheading,details))


    def setupSound(self, defObject):
        """return the sound extension if the dictionary returns a sound, otherwise return -1"""
        sound = defObject.data.get("sound")
        if sound is not None:
            prefix = sound[0]
            if prefix != defObject.data.get("id").lower()[0]:
                for letter in sound[1:]:
                    if letter != defObject.data["id"].lower()[0]:
                        prefix+=letter
                    else:
                        break
            sound = sound.split()[0]
            defObject.data["sound"] = prefix+"/"+sound
            
    def checkForAndRemoveLeadingColon(self, details, subheading):
        if details[0].text[0] == ":":
            text,effect = details.pop(0)
            details.insert(0, HTMLString(text[1:],effect))

    
 

DefinitionTuple = namedtuple('DefinitionTuple', 'heading, subheading, details') #Makes the processing cleaner on the template
HTMLStringTuple = namedtuple('HTMLString','text, effect') #DON'T CALL THIS DIRECTLY

def HTMLString(text="", effect=None):
    """
function acting as constructor for HTMLStringTuples
Effect can be additional text effects such as italic or bold

Effect options currently implemented:
    i - italics
    s - strong (bold)
    vt - Verb type change
    """
    return HTMLStringTuple(text,effect)

   
class DefinitionEntry():
    """simple wrapper around a dictionary with a convenience function added in"""
    keys = {
        "hw":"id",
        "fl":"partOfSpeech",
        "pr":"pronunciation",
        "sound/wav":"sound",
        "et":"etymology",
        "date":"date",
    }
    
    def __init__(self):
        """Creates and empty list to hold multiple definitionTuples"""
        self.data = {"definitions":list()}

    def addItem(self, key, item):
        """Properly adds a non definition item to the Definition Entity"""
        self.data[self.keys[key]] = item