import os

def xmllint(osisxml):
    return os.system("xmllint --noout --schema osisCore.2.1.1-cw-latest.xsd.xml " + osisxml)


def test_answer(modulexml):
    assert xmllint(modulexml) == 0
