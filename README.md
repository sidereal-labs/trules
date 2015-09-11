# tRules
Expanded set of Unciode CLDR "Transform Rules" in LDML (XML) format located in transforms directory. Cludgy python parser for testing and other helper scripts contained in ./trules executable. Full list of Unicode script blocks in TODO with initials of contributor of transliteration file (U=Unicode provided transliteration).

There is no promise that these transliteration files are accurate or complete or are fully compatible with Unicode/CLDR/ICU/LDML.

The Unicode provided transliteration rules are contained in the `transforms/cldr` subdirectory, new or extended transliteration rules produeced as a part of this project are in the `transforms` directory itself. 

##Usage
The `trules` executable has three main uses. 

1. The default use is to run through the words and "testdata.txt" and print out transliteration results. A different file of test data can be specified with the `-t` flag.
	* Example: `trules -t othertestdata.txt`

2. The `-c` flag will create a new LDML-like template in the `transforms` directory. Use a hyphen-separated string to be used as the filename (the script will append the .xml) following the pattern SOURCE-TARGET-VARIANT or just SOURCE-TARGET if no variant needs to be specified. 
	* Example: `trules -c Martian-Venutian-UNGEGN`

3. The `-r` flag will rebuild the transliteration models from the `transforms` directory. This is necessary any time an xml file has been added or edited.
	* Example: `trules -r`


#####Help Command 

```
trules [-h] [-r] [-t <TESTFILE>] [-c <SOURCE>-<TARGET>-<VARIANT>]

Transliterate some letters.

optional arguments:
  -h, --help            show this help message and exit
  -r, --rebuild-transforms
                        Reparse xml files into transforms.json in
                        ./transforms/ and ./transforms/cldr/ folders before
                        running tests. Default=FALSE
  -t <TESTFILE>, --test-file <TESTFILE>
                        Test rules transforms.json on list of sample words.
                        Default=testdata.txt
  -c <SOURCE>-<TARGET>-<VARIANT>, --create-xml <SOURCE>-<TARGET>-<VARIANT>
                        Create an empty xml template in the transforms folder
                        for a new ruleset
```

## Helpful Links

* [Unicode Transliteration Guidelines](http://cldr.unicode.org/index/cldr-spec/transliteration-guidelines)
* [Unicode LDML Specifications: Transforms](http://www.unicode.org/reports/tr35/tr35-general.html#Transforms)
* [Unicode Utilities: Transforms](http://unicode.org/cldr/utility/transform.jsp)
* [ICU Transform Demonstration](http://demo.icu-project.org/icu-bin/translit)
* [ICU User Guide: General Transforms](http://userguide.icu-project.org/transforms/general)
* [UNITED NATIONS GROUP OF EXPERTS ON GEOGRAPHICAL NAMES (UNGEGN) Working Group on Romanization Systems](http://www.eki.ee/wgrs/)
					
