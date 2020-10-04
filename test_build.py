import os
import configparser
import re
from collections import OrderedDict
import tempfile
import shutil
import pytest
import subprocess

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




def xmllint(osisxml):
    return os.system("xmllint --noout --schema osisCore.2.1.1-cw-latest.xsd.xml " + osisxml)


#def test_xmllint(modulexml):
#    assert xmllint(modulexml) == 0

def test_sword_build(modulexml):
    print('')
    dirpath = tempfile.mkdtemp()
    moduledir = re.sub(r'\.[^\.]+$', r'', os.path.basename(pytest.moduleconf))
    module_target = '{}/build/modules/texts/ztext/{}'.format(dirpath, moduledir)
    os.makedirs(module_target)
    os.makedirs('{}/build/mods.d'.format(dirpath))
    shutil.copyfile(pytest.moduleconf, '{}/build/mods.d/{}'.format(dirpath, os.path.basename(pytest.moduleconf)))
    versification = 'KJV'
    try:
      versification = pytest.config[pytest.modulename]['Versification']
    except:
      pass
    osis2mod_result = subprocess.run(['osis2mod', module_target, modulexml, '-v', versification, '-z'], stdout=subprocess.PIPE, stderr=subprocess.PIPE )
    #osis2mod  build/modules/texts/ztext/hunkal osis.xml -v Vulg -z 2>/dev/null
    stdout = osis2mod_result.stdout.decode('utf-8')
    stderr = osis2mod_result.stderr.decode('utf-8')
    versification_issues = 0
    reference_errors = 0
    other_issues = []

    for line in stdout.split('\n'):
        if re.search(r'^INFO\(V11N\)', line):
            versification_issues = versification_issues + 1
        elif re.search(r'^ERROR\(REF\)', line):
            reference_errors = reference_errors + 1
        elif re.search(r'^INFO\(WRITE\)', line):
            pass
        elif re.search(r'^WARNING\(UTF8\): osis2mod is not compiled with support for ICU. Assuming -N.', line):
            pass
        elif re.search(r'^$', line):
            pass
        else:
            other_issues.append(line)
    print('{} versification issues {} reference_errors {} other issues {}'.format(versification, versification_issues, reference_errors, len(other_issues)))

    #shutil.rmtree(dirpath)
    assert osis2mod_result.returncode == 0


def test_sword_alternate_versifications(modulexml):
    print('')
    for versification in ['Calvin','Catholic','Catholic2','Darby_fr','German','KJV','KJVA','LXX','Leningrad','Luther','MT','NRSV','NRSVA','Orthodox','Segond','Synodal','SynodalProt','Vulg']:
        dirpath = tempfile.mkdtemp()
        moduledir = re.sub(r'\.[^\.]+$', r'', os.path.basename(pytest.moduleconf))
        module_target = '{}/build/modules/texts/ztext/{}'.format(dirpath, moduledir)
        os.makedirs(module_target)
        os.makedirs('{}/build/mods.d'.format(dirpath))
        shutil.copyfile(pytest.moduleconf, '{}/build/mods.d/{}'.format(dirpath, os.path.basename(pytest.moduleconf)))

        osis2mod_result = subprocess.run(['osis2mod', module_target, modulexml, '-v', versification, '-z'], stdout=subprocess.PIPE, stderr=subprocess.PIPE )
        #osis2mod  build/modules/texts/ztext/hunkal osis.xml -v Vulg -z 2>/dev/null
        stdout = osis2mod_result.stdout.decode('utf-8')
        stderr = osis2mod_result.stderr.decode('utf-8')
        versification_issues = 0
        reference_errors = 0
        other_issues = []

        for line in stdout.split('\n'):
            if re.search(r'^INFO\(V11N\)', line):
                versification_issues = versification_issues + 1
            elif re.search(r'^ERROR\(REF\)', line):
                reference_errors = reference_errors + 1
            elif re.search(r'^INFO\(WRITE\)', line):
                pass
            elif re.search(r'^WARNING\(UTF8\): osis2mod is not compiled with support for ICU. Assuming -N.', line):
                pass
            elif re.search(r'^$', line):
                pass
            else:
                other_issues.append(line)
        print('{} versification issues {} reference_errors {} other issues {}'.format(versification, versification_issues, reference_errors, len(other_issues)))
        #if(len(other_issues) > 0):
        #    print('other issues (top)')
        #    print(other_issues[:5])

        shutil.rmtree(dirpath)
    assert True
