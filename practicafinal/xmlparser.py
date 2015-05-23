from xml.sax.handler import ContentHandler
from xml.sax import parseString
from datetime import date, time

class actsHandler(ContentHandler):
    def __init__(self):
        self.inContent = False
        self.theContent = ""
        self.inEvent = False
        self.inTitle = False
        self.inType = False
        self.inFree = False
        self.inPrice = False
        self.inDate = False
        self.inTime = False
        self.inLong = False
        self.inUrl = False
        self.activity = {}
        self.acts = []


    def checkAttrs(self, attrs):
        if attrs.getValue("nombre") == "TITULO":
            self.inContent = True
            self.inTitle = True
        elif attrs.getValue("nombre") == "TIPO":
            self.inContent = True
            self.inType = True
        elif attrs.getValue("nombre") == "GRATUITO":
            self.inContent = True
            self.inFree = True
        elif attrs.getValue("nombre") == "PRECIO":
            self.inContent = True
            self.inPrice = True
        elif attrs.getValue("nombre") == "FECHA-EVENTO":
            self.inContent = True
            self.inDate = True
        elif attrs.getValue("nombre") == "HORA-EVENTO":
            self.inContent = True
            self.inTime = True
        elif attrs.getValue("nombre") == "EVENTO-LARGA-DURACION":
            self.inContent = True
            self.inLong = True
        elif attrs.getValue("nombre") == "CONTENT-URL":
            self.inContent = True
            self.inUrl = True


    def checkCases(self):
        if self.inTitle:
            self.inTitle = False
            self.inContent = False
            self.activity['title'] = self.theContent
            self.theContent = ""
        elif self.inType:
            self.inType = False
            self.inContent = False
            self.activity['type'] = self.theContent
            self.theContent = ""
        elif self.inFree:
            self.inFree = False
            self.inContent = False
            self.activity['free'] = self.theContent
            self.theContent = ""
        elif self.inPrice:
            self.inPrice = False
            self.inContent = False
            self.activity['price'] = self.theContent
            self.theContent = ""
        elif self.inDate:
            self.inDate = False
            self.inContent = False
            self.theContent = self.theContent.split("-")
            year = int(self.theContent[0])
            month = int(self.theContent[1])
            day = int(self.theContent[2].split(" ")[0])
            self.activity['date'] = date(year, month, day)
            self.theContent = ""
        elif self.inTime:
            self.inTime = False
            self.inContent = False
            hour = int(self.theContent.split(':')[0])
            minutes = int(self.theContent.split(':')[1])
            self.activity['time'] = time(hour, minutes)
            self.theContent = ""
        elif self.inLong:
            self.inLong = False
            self.inContent = False
            self.activity['long'] = self.theContent
            self.theContent = ""
        elif self.inUrl:
            self.inUrl = False
            self.inContent = False
            self.activity['url'] = self.theContent
            self.theContent = ""


    def startElement(self, name, attrs):
        if name == "contenido":
            self.inEvent = True
        elif self.inEvent and name != 'tipo':
            if attrs.has_key('nombre'):
                self.checkAttrs(attrs)


    def endElement(self, name):
        if name == "contenido":
            self.inEvent = False
            self.acts.append(self.activity)
            self.activity = {}
        elif self.inEvent:
            self.checkCases()


    def characters(self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars


def parse(xml):
    handler = actsHandler()
    parseString(xml, handler)
    return handler.acts
