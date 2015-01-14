#!/usr/bin/env python

import re
import sys
import os
import json
import math
import random

speeches = open("input.txt")



def speechYielder():
    lastYear = None
    currentArray = []

    for line in speeches:
        line = line.rstrip("\n")
        parts = line.split("\t")
        text = parts[1]
        filename = parts[0]
        (year,paragraph) = parts[0].split("/")
        if lastYear != year:
            yield(currentArray)
            currentArray = []
        lastYear = year
        searchstring = "<span class=SOTUyear>%s</span><span class=paragraph>, paragraph %s</span>: <span class=text>%s</span>" %(year,paragraph,text)
        currentArray.append({
            "filename":filename,
            "searchstring":searchstring,
            "year":int(year),
            "paragraph":int(paragraph)
            })


    yield(currentArray)



for speech in speechYielder():
    totalLength = len(speech)
    for paragraph in speech:
        paragraph["twelfth"] = ((1+paragraph["paragraph"])*12)/totalLength
        print json.dumps(paragraph)
        pass
