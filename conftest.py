# content of conftest.py
import pytest

def pytest_addoption(parser):
    parser.addoption("--modulename", action="store", help="module name to check for")
    parser.addoption("--moduleconf", action="store", help="module config file to check for")
    parser.addoption("--modulexml", action="store", help="module OSIS XML to test")


@pytest.fixture
def modulename(request):
    return request.config.getoption("--modulename")

@pytest.fixture
def moduleconf(request):
    return request.config.getoption("--moduleconf")

@pytest.fixture
def modulexml(request):
    return request.config.getoption("--modulexml")


#def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
 #   option_value = metafunc.config.option.modulename
 #   if 'modulename' in metafunc.fixturenames and option_value is not None:
 #       metafunc.parametrize("modulename", [option_value])
 #   if 'moduleconf' in metafunc.fixturenames and option_value is not None:
 #       metafunc.parametrize("moduleconf", [option_value])
