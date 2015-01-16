import re

for line in open("input.txt"):
    (filename,text) = line.split("\t")
    for match in re.findall("[A-Z][A-Za-z\-]+ Empire",text):
        if match not in ["Central Empire","The Empire","Austro-Hungarian Empire"]:
            print "\t".join([filename,match])
#    for match in re.findall("Empire of (?:the )?[A-Za-z]+",text):
#        print "\t".join([filename,match])
    for match in re.findall("Austro-Hungarian",text):
        print "\t".join([filename,match])

