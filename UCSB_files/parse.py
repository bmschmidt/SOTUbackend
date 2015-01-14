from BeautifulSoup import BeautifulSoup
import sys

soup = BeautifulSoup(open(sys.argv[1]))

span = soup.findAll('span', {'class':'displaytext'})[0]

paras = [x for x in span.findAllNext("p")]

start = span.string
middle = "\n\n".join(["".join(x.findAll(text=True)) for x in paras[:-1]])
last = paras[-1].contents[0]
out =  "%s\n\n%s\n\n%s" % (start, middle, last)

print out.encode("utf-8")

