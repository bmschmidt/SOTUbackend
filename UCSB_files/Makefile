YEARS= $(shell awk '{print $$2}' speeches.txt | sort)
SPEECHES = $(addprefix speeches/,$(addsuffix .txt,$(YEARS)))
URLS = $(shell awk '{print $$1}' speeches.txt)
DOWNLOADS = $(addsuffix .html, $(URLS))

CHUNKED = $(addprefix chunked/, $(YEARS))

all: $(SPEECHES)

redownload: $(DOWNLOADS)

quick: $(CHUNKED)

sou.php:
	wget http://www.presidency.ucsb.edu/sou.php

speeches.txt: sou.php
#List of all the speeches
	cat sou.php | perl -ne 'if ($$_ =~ m/http.*pid=(\d+)">(\d\d\d\d)\</) {print $$1 . "\t" . $$2 . "\n"}' > speeches.txt

htmls/%.html:
	sleep 2
	curl http://www.presidency.ucsb.edu/ws/index.php?pid=$(notdir$(basename $@)) > $@

speeches/%.txt:
	python parse.py htmls/$$(awk '{if ($$2=="$(notdir $(basename $@))") {print $$1}}' speeches.txt).html > $@

jsoncatalog.txt: input.txt
	python catalogify.py > jsoncatalog.txt

clean:
	rm -r chunked/*
	rm $(FORMATTED)
	rm $(HTMLS)
	rm $(SPEECHES)

input.txt:
	python chunker.py $(SPEECHES) > input.txt

bookworm: jsoncatalog.txt
	mkdir -p ~/SOTU/files
	mkdir -p ~/SOTU/files/metadata
	mkdir -p ~/SOTU/files/texts
	rm -rf ~/SOTU/files/texts/raw
	cp jsoncatalog.txt ~/SOTU/files/metadata/jsoncatalog.txt
	cp input.txt ~/SOTU/files/texts
	cp field_descriptions.json ~/SOTU/files/metadata
