# tRules
Expanded set of Unciode CLDR "Transform Rules" in LDML (XML) format located in transforms directory. Cludgy python parser for testing and other helper scripts contained in ./trules executable. Full list of Unicode script blocks in TODO with initials of contributor of transliteration file (U=Unicode provided transliteration).

There is no promise that these transliteration files are accurate or complete or are fully compatible with Unicode/CLDR/ICU/LDML.

## ./trules --help

```trules [-h] [-r] [-t <TESTFILE>] [-c <SOURCE>-<TARGET>-<VARIANT>]

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
                        for a new ruleset```

## Helpful Links

* [Unicode Transliteration Guidelines](http://cldr.unicode.org/index/cldr-spec/transliteration-guidelines)
* [Unicode LDML Specifications: Transforms](http://www.unicode.org/reports/tr35/tr35-general.html#Transforms)
* [Unicode Utilities: Transforms](http://unicode.org/cldr/utility/transform.jsp)
* [ICU Transform Demonstration](http://demo.icu-project.org/icu-bin/translit)
* [ICU User Guide: General Transforms](http://userguide.icu-project.org/transforms/general)
* [UNITED NATIONS GROUP OF EXPERTS ON GEOGRAPHICAL NAMES (UNGEGN) Working Group on Romanization Systems](http://www.eki.ee/wgrs/)
					
