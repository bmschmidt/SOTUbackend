sources=$(shell find txts -type f -name "*.txt")


all:  bookwormBuilt supplementsBuilt


pristine:
	cd SOTUgeo; make pristine;
	-rm bookwormBuilt
	-rm supplementsBuilt
	make cleanSup



input.txt: UCSB_files/input.txt
	cp $< $@

field_descriptions.json: UCSB_files/field_descriptions.json
	cp $< $@

jsoncatalog.txt: UCSB_files/jsoncatalog.txt
	cp $< $@

all: bookwormBuilt

SOTUgeo:
	git clone git@github.com:bmschmidt/Presidio SOTUgeo

bookwormPreconditions: SOTUgeo targets SOTUgeo/files/metadata/jsoncatalog.txt SOTUgeo/files/texts/input.txt SOTUgeo/files/metadata/field_descriptions.json

targets:
	mkdir -p SOTUgeo/files/metadata
	mkdir -p SOTUgeo/files/texts

SOTUgeo/files/metadata/field_descriptions.json: field_descriptions.json
	cp $< $@

SOTUgeo/files/metadata/jsoncatalog.txt: jsoncatalog.txt
	cp $< $@

SOTUgeo/files/texts/input.txt: input.txt
	cp $< $@

cleanworm:
	rm -rf SOTUgeo/files/targets/database*;
	rm -f bookworm

SOTUgeo/extensions:
	cp -r extensions $@

cleanSup:
	rm -f SOTUgeo/extensions/geotagger/metadata.txt
	rm -f SOTUgeo/extensions/bookworm-geotagger/geocoded.txt

SOTUgeo/extensions/geotagger/metadata.txt: SOTUgeo/files/texts/input.txt
	cd SOTUgeo/extensions/geotagger ; make clean;
	cd SOTUgeo/extensions/geotagger ; make;
#At this point, there is a file in the destination; but then we update it with some hand tweaks
	make betterMetadata.txt
	mv betterMetadta.txt $@

SOTUgeo/extensions/bookworm-geolocator/geocoded.txt: SOTUgeo/extensions/geotagger/metadata.txt
	cd SOTUgeo/extensions/bookworm-geolocator; make;

bookwormBuilt: bookwormPreconditions SOTUgeo input.txt jsoncatalog.txt Placenames.tsv 
	cd SOTUgeo; make;
	touch bookwormBuilt

supplementsBuilt: bookwormBuilt SOTUgeo/extensions SOTUgeo/extensions/geotagger/metadata.txt SOTUgeo/extensions/bookworm-geolocator/geocoded.txt
	cd SOTUgeo; python OneClick.py supplementMetadataFromJSON extensions/geotagger/metadata.txt filename
	cd SOTUgeo; python OneClick.py supplementMetadataFromTSV extensions/bookworm-geolocator/geocoded.txt
#Add the party information.
	cd SOTUgeo; python OneClick.py supplementMetadataFromTSV ../UCSB_files/parties.tsv
	touch $@

fullCorrectives.tsv: correctiveTSV.tsv
#Mitch's corrections should have added on, at the end, my grep after empire names.
	cat $< > $@
#And then grep out empires in particular.
	python specialEmpireException.py >> $@

betterMetadata.txt: SOTUgeo/extensions/geotagger/metadata.txt fullCorrectives.tsv
#read in the metadata file, and supplement the locations with new ones.
	python incorporateHandPlaceAdditions.py > $@


Placenames.tsv:
#Get a master list of placenames from Mitch's CSV file.
#Obsolete--this data is now being stored in my NER repository.
	echo "LOCATION	mentionedPoint	placetype" > Placenames.tsv
	LC_ALL='C'; perl -pe 's/\r/\n/g; s/\d{4,},([^,]+),"(.+)",(.+)/$$1\t[$$2]\t$$3/g' StateoftheUnionGeocoded.csv | sort | uniq | grep "	" >> Placenames.tsv
