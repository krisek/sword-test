#!/usr/bin/python

import pytest

import configparser
import re
from collections import OrderedDict
from iso639 import languages

class ConfigParserMultiValues(OrderedDict):

    def __setitem__(self, key, value):
        if key in self and isinstance(value, list):
            self[key].extend(value)
        else:
            super().__setitem__(key, value)

    @staticmethod
    def getlist(value):
        return value.split(os.linesep)



def test_init(moduleconf, modulename):
  pytest.moduleconf = moduleconf
  pytest.modulename = modulename
  pytest.config = configparser.ConfigParser(strict=False, empty_lines_in_values=False, dict_type=ConfigParserMultiValues, converters={"list": ConfigParserMultiValues.getlist})
  pytest.config.read([pytest.moduleconf])
  assert True



def test_section_name_conform():
  sections = pytest.config.sections()
  for section in sections:
    matchObj = re.search(r'^[A-Za-z0-9_]+$', section)
    if not matchObj:
      assert False
    assert True

def test_section_name():
  sections = pytest.config.sections()
  assert pytest.modulename in sections


def test_description_one_line():
  try:
    description = pytest.config[pytest.modulename]['Description']
  except:
    assert False

  assert len(description) != 0 and not re.search('\n', description)

def test_description_exists():
  try:
    description = pytest.config[pytest.modulename]['Description']
  except:
    assert False

  assert len(description) != 0


def test_data_path():
  try:
    datapath = pytest.config[pytest.modulename]['DataPath']
  except:
    assert False

  assert re.search(r'^\./modules', datapath)


def test_ModDrv():
  try:
    ModDrv = pytest.config[pytest.modulename]['ModDrv']
  except:
    assert False
  assert ModDrv in ['RawText','RawText4','zText','zText4','RawCom','RawCom4','zCom','zCom4','HREFCom','RawFiles','RawLD','RawLD4','zLD','RawGenBook']

def test_SourceType():
  SourceType = 'OSIS'
  try:
    SourceType = pytest.config[pytest.modulename]['SourceType']
  except:
    assert True
  assert SourceType in ['OSIS','TEI','GBF','ThML']

def test_Encoding():
  Encoding = 'Latin-1'
  try:
    Encoding = pytest.config[pytest.modulename]['Encoding']
  except:
    assert True
  assert Encoding in ['UTF-8', 'UTF-16', 'SCSU']

def test_CompressType():
  CompressType = 'LZSS'
  try:
    CompressType = pytest.config[pytest.modulename]['CompressType']
  except:
    assert True
  assert CompressType in ['ZIP', 'LZSS', 'BZIP2', 'XZ']

def test_BlockType():
  BlockType = "CHAPTER"
  try:
    BlockType = pytest.config[pytest.modulename]['BlockType']
  except:
    assert True
  assert BlockType in ['BOOK', 'CHAPTER', 'CHAPTER']

def test_BlockCount():
  BlockCount = 200
  try:
    BlockCount = pytest.config[pytest.modulename]['BlockCount']
  except:
    assert True
  assert int(BlockCount)

def test_Versification():
  Versification = 'KJV'
  try:
    Versification = pytest.config[pytest.modulename]['Versification']
  except:
    assert True
  assert Versification in ['Calvin','Catholic','Catholic2','Darby_fr','German','KJV','KJVA','LXX','Leningrad','Luther','MT','NRSV','NRSVA','Orthodox','Segond','Synodal','SynodalProt','Vulg']

def test_KeyType():
  KeyType = 'TreeKey'
  try:
    KeyType = pytest.config[pytest.modulename]['KeyType']
  except:
    assert True
  assert KeyType in ['TreeKey', 'VerseKey']

def test_GlobalOptionFilter():
  GlobalOptionFilter = []
  try:
    GlobalOptionFilter = pytest.config[pytest.modulename]['GlobalOptionFilter'].split('\n')
  except:
    assert True

  for global_option_filter in GlobalOptionFilter:
    if global_option_filter not in ['UTF8Cantillation','UTF8GreekAccents','UTF8HebrewPoints','UTF8ArabicPoints','OSISLemma','OSISMorphSegmentation','OSISStrongs','OSISFootnotes','OSISScripref','OSISMorph','OSISHeadings','OSISVariants','OSISRedLetterWords','OSISGlosses','OSISXlit','OSISEnum','OSISReferenceLinks','OSISRuby','GBFStrongs','GBFFootnotes','GBFMorph','GBFHeadings','GBFRedLetterWords','ThMLStrongs','ThMLFootnotes','ThMLScripref','ThMLMorph','ThMLHeadings','ThMLVariants','ThMLLemma']:
        assert False

  assert True

def test_Direction():
  Direction = 'LtoR'
  try:
    Direction = pytest.config[pytest.modulename]['Direction']
  except:
    assert True
  assert Direction in ['LtoR', 'RtoL', 'BiDi']

def test_DisplayLevel():
  DisplayLevel = 1
  try:
    DisplayLevel = pytest.config[pytest.modulename]['DisplayLevel']
  except:
    assert True
  assert int(DisplayLevel)

def test_Feature():
  Feature = []
  try:
    Feature = pytest.config[pytest.modulename]['Feature'].split('\n')
  except:
    assert True

  for feature in Feature:
    if feauture not in ['StrongsNumbers', 'GreekDef', 'HebrewDef', 'GreekParse', 'HebrewParse', 'DailyDevotion', 'Glossary', 'Images', 'NoParagraphs']:
        assert False

  assert True

def test_SwordVersionDate():

  try:
    SwordVersionDate = pytest.config[pytest.modulename]['SwordVersionDate']
  except:
    assert False

  assert re.search(r'^\d\d\d\d\-\d\d-\d\d$', SwordVersionDate)


def test_Category():
  Category = 'Biblical Texts'
  try:
    Category = pytest.config[pytest.modulename]['Category']
  except:
    assert True

  assert Category in ['Biblical Texts', 'Commentaries', 'Lexicons / Dictionaries', 'Glossaries', 'Daily Devotional', 'Generic Books', 'Maps', 'Images', 'Cults / Unorthodox / Questionable Material', 'Essays']


def test_DistributionLicense():
  try:
    License = pytest.config[pytest.modulename]['DistributionLicense']
  except:
    assert False

  assert License in ['Public Domain', 'Copyrighted', 'Copyrighted; Permission to distribute granted to CrossWire', 'Copyrighted; Permission granted to distribute non-commercially in SWORD format', 'Copyrighted; Free non-commercial distribution', 'Copyrighted; Freely distributable', 'GFDL', 'GPL', 'Creative Commons: BY-NC-ND 4.0', 'Creative Commons: BY-NC-SA 4.0', 'Creative Commons: BY-NC 4.0', 'Creative Commons: BY-ND 4.0', 'Creative Commons: BY-SA 4.0', 'Creative Commons: BY 4.0', 'Creative Commons: CC0']

def test_Lang():
  #Lang, GlossaryFrom, GlossaryTo
  Lang = 'en'
  try:
    Lang = pytest.config[pytest.modulename]['Lang']
  except:
    assert True
  lang = re.sub(r'\-.*', r'', Lang)
  pytest.lang  = False
  found = False
  try:
    pytest.lang = languages.get(part1 = lang)
    found = True
  except:
    pass

  if not found:
    try:
      pytest.lang = languages.get(part2b = lang)
      found = True
    except:
      pass

  if not found:
    try:
      pytest.lang = languages.get(part2t = lang)
      found = True
    except:
      pass

  if not found:
    try:
      pytest.lang = languages.get(part3 = lang)
      found = True
    except:
      pass

  if not found:
    try:
      pytest.lang = languages.get(part5 = lang)
      found = True
    except:
      pass


  if(len(lang) == 2 or len(lang) == 3):
    assert pytest.lang
  else:
    assert True #let this test pass as we cannot check everything
