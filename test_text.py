import pytest
import configparser
from collections import OrderedDict
import re
import xml.dom.minidom
from string import punctuation
from iso639 import languages


pytest.bible_books = ['Gen', 'Exod', 'Lev', 'Num', 'Deut', 'Josh', 'Judg', 'Ruth', '1Sam', '2Sam', '1Kgs', '2Kgs', '1Chr', '2Chr', 'Ezra', 'Neh', 'Tob', 'Jdt', 'Esth', 'Job', 'Ps', 'Prov', 'Eccl', 'Song', 'Wis', 'Sir', 'Isa', 'Jer', 'Lam', 'Bar', 'Ezek', 'Dan', 'Hos', 'Joel', 'Amos', 'Obad', 'Jonah', 'Mic', 'Nah', 'Hab', 'Zeph', 'Hag', 'Zech', 'Mal', '1Macc', '2Macc', 'Matt', 'Mark', 'Luke', 'John', 'Acts', 'Rom', '1Cor', '2Cor', 'Gal', 'Eph', 'Phil', 'Col', '1Thess', '2Thess', '1Tim', '2Tim', 'Titus', 'Phlm', 'Heb', 'Jas', '1Pet', '2Pet', '1John', '2John', '3John', 'Jude', 'Rev']



class ConfigParserMultiValues(OrderedDict):

    def __setitem__(self, key, value):
        if key in self and isinstance(value, list):
            self[key].extend(value)
        else:
            super().__setitem__(key, value)

    @staticmethod
    def getlist(value):
        return value.split(os.linesep)

pytest.xmltext=''
pytest.lang  = None
pytest.xml = None

pytest.xml_xmlns_xsi = ''
pytest.xml_xmlns = ''
pytest.xml_xmlns_osis = ''
pytest.xml_xsi_schemaLocation = ''


def find_language(lang):

  found = False
  print(lang)
  try:
    lang_639 = languages.get(part1 = lang)
    found = True
  except:
    pass

  if not found:
    try:
      lang_639 = languages.get(part2b = lang)
      found = True
    except:
      pass

  if not found:
    try:
      lang_639 = languages.get(part2t = lang)
      found = True
    except:
      pass

  if not found:
    try:
      lang_639 = languages.get(part3 = lang)
      found = True
    except:
      pass

  if not found:
    try:
      lang_639 = languages.get(part5 = lang)
      found = True
    except:
      pass
  return (lang_639, found)

def test_readfile(modulexml):
    with open(modulexml, 'r') as reader:
      pytest.xmltext = reader.read()
    pytest.xml = xml.dom.minidom.parse(modulexml);
    assert True

def test_init(moduleconf, modulename):
  pytest.moduleconf = moduleconf
  pytest.modulename = modulename
  pytest.config = configparser.ConfigParser(strict=False, empty_lines_in_values=False, dict_type=ConfigParserMultiValues, converters={"list": ConfigParserMultiValues.getlist})
  pytest.config.read([pytest.moduleconf])

  #get module language
    #Lang, GlossaryFrom, GlossaryTo
  Lang = 'en'
  try:
    Lang = pytest.config[pytest.modulename]['Lang']
  except:
    pass

  lang = re.sub(r'\-.*', r'', Lang)

  (pytest.lang, found) = find_language(lang)

  assert found



def test_aphostrophes_1(modulexml):
    aphostrophes = pytest.xmltext.count('"')
    assert aphostrophes % 2 == 0

#https://op.europa.eu/en/web/eu-vocabularies/formex/physical-specifications/character-encoding/use-of-quotation-marks-in-the-different-languages
def test_aphostrophes_bul(modulexml): #bulgarian
    if pytest.lang and pytest.lang.part1 in ['bg', 'cz', 'et', 'de', 'is', 'lt', 'sk', 'sl']:
      assert pytest.xmltext.count('„') == pytest.xmltext.count('“')

def test_aphostrophes_dutch(modulexml): #dutch
    if pytest.lang and pytest.lang.part1 in ['nl', 'en-IE', 'lv', 'mt']:
        assert pytest.xmltext.count('“') == pytest.xmltext.count('”')

def test_aphostrophes_5(modulexml): #english
    #if pytest.lang and pytest.lang.part1 in ['en']:
    assert pytest.xmltext.count('‘') == pytest.xmltext.count('’')

def test_aphostrophes_6(modulexml): #finish, swedish
    if pytest.lang and pytest.lang.part1 in ['fi', 'sv']:
        assert pytest.xmltext.count('”') % 2 == 0

def test_aphostrophes_7(modulexml): #french, spanish, portugese, greek italian «...» danish »...«
    assert pytest.xmltext.count('«') == pytest.xmltext.count('»')

def test_aphostrophes_8(modulexml): #hungarian, polish, romanian, croatian
    if pytest.lang and pytest.lang.part1 in ['hu', 'ro', 'pl', 'hr']:
        assert pytest.xmltext.count('„') == pytest.xmltext.count('”')

def test_osis_attributes():
    if pytest.xml:
        for osis in pytest.xml.getElementsByTagName('osis'):
            pytest.xml_xmlns_xsi = osis.getAttribute('xmlns:xsi')
            pytest.xml_xmlns = osis.getAttribute('xmlns')
            pytest.xml_xmlns_osis = osis.getAttribute('xmlns:osis')
            pytest.xml_xsi_schemaLocation = osis.getAttribute('xsi:schemaLocation')
            break


def test_osis_xmlns_xsi():
    if pytest.xml_xmlns_xsi != '':
        assert pytest.xml_xmlns_xsi == 'http://www.w3.org/2001/XMLSchema-instance'

def test_osis_xmlns():
    if pytest.xml_xmlns != '':
        assert pytest.xml_xmlns == 'http://www.bibletechnologies.net/2003/OSIS/namespace'

def test_osis_xmlns_osis():
    if pytest.xml_xmlns_osis != '':
        assert pytest.xml_xmlns_osis == 'http://www.bibletechnologies.net/2003/OSIS/namespace'

def test_osis_xsi_schemaLocation():
    if pytest.xml_xsi_schemaLocation!= '':
        assert pytest.xml_xsi_schemaLocation == 'http://www.bibletechnologies.net/2003/OSIS/namespace https://www.crosswire.org/osis/osisCore.2.1.1.xsd'

def test_osis_references_1():
    nonconform_references = []
    for reference in pytest.xml.getElementsByTagName('reference'):
        osisRef = reference.getAttribute('osisRef')
        osisRefText = reference.firstChild.data
        if re.search(r'\-', osisRef) is not None and re.search(r'\-', osisRefText) is not None:
            continue
        if re.search(r'\-', osisRef) is None and re.search(r'\-', osisRefText) is None:
            continue
        nonconform_references.append({'verse': reference.parentNode.parentNode.getAttribute('osisID'), 'ref': osisRef})

    assert nonconform_references == []

def test_osis_references_2():
    invalid_references = []
    osisIDs = []
    #get osisIDs
    for verse in pytest.xml.getElementsByTagName('verse'):
        osisIDs.append(verse.getAttribute('osisID'))

    for reference in pytest.xml.getElementsByTagName('reference'):
        osisRef = reference.getAttribute('osisRef')
        osisRefText = reference.firstChild.data
        matchObj = re.search(r'^(\w+\.\d+\.\d+)\-(\w+\.\d+\.\d+)$', osisRef)

        if matchObj:
            if(matchObj[1] not in osisIDs):# or matchObj[2] not in osisIDs):
                invalid_references.append({'verse': reference.parentNode.parentNode.getAttribute('osisID'), 'ref': osisRef})


        else:
            matchObj = re.search(r'^(\w+\.\d+\.\d+)$', osisRef)
            if matchObj:
                if(matchObj[1] not in osisIDs):
                    invalid_references.append({'verse': reference.parentNode.parentNode.getAttribute('osisID'), 'ref': osisRef})


        if(matchObj is None):
            invalid_references.append({'verse': reference.parentNode.parentNode.getAttribute('osisID'), 'ref': osisRef})

    assert invalid_references == []

def test_empty_verses_1():
    verses_with_no_text = []

    for verse in pytest.xml.getElementsByTagName('verse'):
        if  verse.firstChild is None or verse.firstChild.data is None:
            verses_with_no_text.append(verse.getAttribute('osisID'))
    assert verses_with_no_text == []

def test_punctuation_1():
    punctuation_issues = []
    for verse in pytest.xml.getElementsByTagName('verse') + pytest.xml.getElementsByTagName('title'):
        if  verse.firstChild is not None and re.search(r'([\.\,\;\:][^\s“”’»«\)])', verse.firstChild.data):
            matchObj = re.search(r'([\.\,\;\:][^\s“”’»«\)])', verse.firstChild.data)
            punctuation_issues.append({verse.getAttribute('osisID'): matchObj[1]})

    #print(punctuation_issues)
    assert len(punctuation_issues) == 0

def test_alphanum_1():
    verses_with_strange_characters = []
    apostrophes = "„“”‘’«»"
    dashes = "-–—"

    for verse in pytest.xml.getElementsByTagName('verse') + pytest.xml.getElementsByTagName('title') + pytest.xml.getElementsByTagName('reference'):
        verse_normalized_text = ""
        if  verse.firstChild is None or verse.firstChild.data is None:
            continue
            #verse_normalized_text = normalize('NFC', verse.firstChild.data)
        verse_normalized_text = verse.firstChild.data
        non_matching = re.findall(r'[^\w\d {}{}{}\n]+'.format(re.escape(punctuation), apostrophes, re.escape(dashes)), verse_normalized_text, flags=re.IGNORECASE|re.UNICODE)
        if len(non_matching) > 0:
            verses_with_strange_characters.append({
                'non_matching': non_matching,
                'verse': verse_normalized_text,
                'osisID': verse.getAttribute('osisID')
            })

    assert verses_with_strange_characters == []

def test_versification_refsystem():
    Versification = pytest.config[pytest.modulename]['Versification']
    refsystem_issues = []
    for refsystem in pytest.xml.getElementsByTagName('refSystem'):
        if refsystem.firstChild.data != 'Bible.' + Versification:
            refsystem_issues.append({'is': refsystem.firstChild.data, 'should': 'Bible.' + Versification})
    assert refsystem_issues == []

"""
<osisText osisText="HunKar" osisRefWork="Bible" xml:lang="hu"  canonical="true">

        <header>
                <work osisWork="HunKar">

"""

def test_osis_identifier():
    identifier = pytest.xml.getElementsByTagName('identifier')[0]
    assert identifier.firstChild.data == 'Bible.' + pytest.modulename

def test_osis_work():
    problematic_osis_work = []
    for work in pytest.xml.getElementsByTagName('work'):
        if work.getAttribute('osisWork') not in [pytest.modulename, 'defaultReferenceScheme']:
            problematic_osis_work.append(work.getAttribute('osisWork'))

    assert problematic_osis_work == []

def test_osis_text_1():
    osisText = pytest.xml.getElementsByTagName('osisText')[0]
    assert  pytest.modulename == osisText.getAttribute('osisIDWork')

def test_osis_text_2():
    osisText = pytest.xml.getElementsByTagName('osisText')[0]
    lang = osisText.getAttribute('xml:lang')
    assert lang == pytest.lang.part1


def test_osis_text_3():
    osisText = pytest.xml.getElementsByTagName('osisText')[0]
    osisRefWork = osisText.getAttribute('osisRefWork')
    assert osisRefWork == 'Bible'



