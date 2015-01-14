#!/usr/bin/env python

import re;

output=open("speeches.txt","w")


seen = dict()

for line in open("sou.php"):
    vals = re.search('http.*pid=(\d+)">(\d\d\d\d)\<',line)
    try:
        m = vals.groups()
        page=m[0]
        year=m[1]


        try:
            done = seen[year]
            print year
            year = str(float(done) + ".1")

            seen[year]=year

        except KeyError:
            seen[year]=year

        output.write(page + "\t" + year + "\n")

    except:
        pass



