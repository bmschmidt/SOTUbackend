import json

years = range(1750,2050)

data = json.load(open("metadata.json"))

fields = ["year","name","party"]

print "\t".join(fields)

for year in years:
    year = str(year)
    try:
        dat = data[year]
    except KeyError:
        continue
    line = [str(dat[field]) for field in fields]
    print "\t".join(line)

