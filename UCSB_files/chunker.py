import sys;
import os;
import re
from HTMLParser import HTMLParser


files = sys.argv[1:]

htmlReplacements = {
    "&#8226;":"'",
    "&frasl;":"/",
    "&mdash;":"--",
    '&lsquo;':"'",
    "&deg;":"o", #Yikes that's not right
    "&frac12;":"1/2", #neither is that, but it isn't as bad.
    "\[[Aa]pplause\]":"",
    "\[[Ll]aughter\]":""
}

def fixHtmls(string):
    for key in htmlReplacements.keys():
        string = re.sub(key,htmlReplacements[key],string)
    return string
    
class handler(object):
    def __init__(self,file):
        self.base = file

    def writeOut(self):
        identifier = re.sub(".txt","",file)
        current = 0
        for para in open(file):
            if len(para) > 2:
                current = current+1
                para = re.sub("\n","",para)
                para = fixHtmls(para)
                
                filename = identifier.replace("speeches/","") + "/" + str(current)
                print "\t".join([filename,para])

if __name__=="__main__":
    for file in files:
        speech = handler(file)
        speech.writeOut()
