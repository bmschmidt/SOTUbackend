import json


def union(a, b):
    """ return the union of two lists """
    return list(set(a+b))

corrections = dict()
for line in open("fullCorrectives.tsv"):
    line = line.rstrip("\n")
    try:
        (key,value) = line.split("\t")
    except ValueError:
        continue
    try:
        corrections[key]= union(corrections[key],[value])
    except KeyError:
        corrections[key] = [value]


for line in open("SOTUgeo/extensions/geotagger/metadata.txt"):
    thisLine = json.loads(line)
    filename = thisLine["filename"]
    if filename not in corrections:
        print json.dumps(thisLine)
        continue
    try:
        thisLine["LOCATION"] = union(thisLine["LOCATION"],corrections[filename])
    except KeyError:
        thisLine["LOCATION"] = corrections[filename]
    del corrections[filename]
    print json.dumps(thisLine)

for key in corrections.keys():
    #Those places that didn't have any NER until now:
    output = dict()
    output["filename"] = key
    output["LOCATION"] = corrections[key]
    print json.dumps(output)
    

