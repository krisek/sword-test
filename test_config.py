#!/usr/bin/python

import pytest

import configparser
import re
from collections import OrderedDict

class ConfigParserMultiValues(OrderedDict):

    def __setitem__(self, key, value):
        if key in self and isinstance(value, list):
            self[key].extend(value)
        else:
            super().__setitem__(key, value)

    @staticmethod
    def getlist(value):
        return value.split(os.linesep)


def get_config(moduleconf):
  config = configparser.ConfigParser(strict=False, empty_lines_in_values=False, dict_type=ConfigParserMultiValues, converters={"list": ConfigParserMultiValues.getlist})
  config.read([moduleconf])
  return config

def test_section_name_conform(modulename, moduleconf):
  config = get_config(moduleconf)
  sections = config.sections()
  for section in sections:
    matchObj = re.search(r'^[A-Za-z0-9_]+$', section)
    if not matchObj:
      assert False
    assert True

def test_section_name(modulename, moduleconf):
  config = get_config(moduleconf)
  sections = config.sections()
  assert modulename in sections


def test_description_one_line(modulename, moduleconf):
  config = get_config(moduleconf)
  try:
    description = config[modulename]['Description']
  except:
    assert False

  assert len(description) != 0 and not re.search('\n', description)

def test_description_exists(modulename, moduleconf):
  config = get_config(moduleconf)
  try:
    description = config[modulename]['Description']
  except:
    assert False

  assert len(description) != 0


def test_data_path(modulename, moduleconf):
  config = get_config(moduleconf)
  try:
    datapath = config[modulename]['DataPath']
  except:
    assert False

  assert re.search(r'^\./modules', datapath)


def test_ModDrv(modulename, moduleconf):
  config = get_config(moduleconf)
  try:
    ModDrv = config[modulename]['ModDrv']
  except:
    assert False
  assert ModDrv in ['RawText','RawText4','zText','zText4','RawCom','RawCom4','zCom','zCom4','HREFCom','RawFiles','RawLD','RawLD4','zLD','RawGenBook']

def test_SourceType(modulename, moduleconf):
  config = get_config(moduleconf)
  SourceType = 'OSIS'
  try:
    SourceType = config[modulename]['SourceType']
  except:
    assert True
  assert SourceType in ['OSIS','TEI','GBF','ThML']

def test_Encoding(modulename, moduleconf):
  config = get_config(moduleconf)
  Encoding = 'Latin-1'
  try:
    Encoding = config[modulename]['Encoding']
  except:
    assert True
  assert Encoding in ['UTF-8', 'UTF-16', 'SCSU']

def test_CompressType(modulename, moduleconf):
  config = get_config(moduleconf)
  CompressType = 'LZSS'
  try:
    CompressType = config[modulename]['CompressType']
  except:
    assert True
  assert CompressType in ['ZIP', 'LZSS', 'BZIP2', 'XZ']

def test_BlockType(modulename, moduleconf):
  config = get_config(moduleconf)
  BlockType = "CHAPTER"
  try:
    BlockType = config[modulename]['BlockType']
  except:
    assert True
  assert BlockType in ['BOOK', 'CHAPTER', 'CHAPTER']

def test_BlockCount(modulename, moduleconf):
  config = get_config(moduleconf)
  BlockCount = 200
  try:
    BlockCount = config[modulename]['BlockCount']
  except:
    assert True
  assert int(BlockCount)

def test_Versification(modulename, moduleconf):
  config = get_config(moduleconf)
  Versification = 'KJV'
  try:
    Versification = config[modulename]['Versification']
  except:
    assert True
  assert Versification in ['Calvin','Catholic','Catholic2','Darby_fr','German','KJV','KJVA','LXX','Leningrad','Luther','MT','NRSV','NRSVA','Orthodox','Segond','Synodal','SynodalProt','Vulg']

def test_KeyType(modulename, moduleconf):
  config = get_config(moduleconf)
  KeyType = 'TreeKey'
  try:
    KeyType = config[modulename]['KeyType']
  except:
    assert True
  assert KeyType in ['TreeKey', 'VerseKey']

def test_GlobalOptionFilter(modulename, moduleconf):
  config = get_config(moduleconf)
  GlobalOptionFilter = []
  try:
    GlobalOptionFilter = config[modulename]['GlobalOptionFilter'].split('\n')
  except:
    assert True

  for global_option_filter in GlobalOptionFilter:
    if global_option_filter not in ['UTF8Cantillation','UTF8GreekAccents','UTF8HebrewPoints','UTF8ArabicPoints','OSISLemma','OSISMorphSegmentation','OSISStrongs','OSISFootnotes','OSISScripref','OSISMorph','OSISHeadings','OSISVariants','OSISRedLetterWords','OSISGlosses','OSISXlit','OSISEnum','OSISReferenceLinks','OSISRuby','GBFStrongs','GBFFootnotes','GBFMorph','GBFHeadings','GBFRedLetterWords','ThMLStrongs','ThMLFootnotes','ThMLScripref','ThMLMorph','ThMLHeadings','ThMLVariants','ThMLLemma']:
        assert False

  assert True

def test_Direction(modulename, moduleconf):
  config = get_config(moduleconf)
  Direction = 'LtoR'
  try:
    Direction = config[modulename]['Direction']
  except:
    assert True
  assert Direction in ['LtoR', 'RtoL', 'BiDi']




