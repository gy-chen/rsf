import os
import pytest

BASE_PATH = os.path.dirname(__file__)


@pytest.fixture
def sample_wiktionary_xml_file_path():
    return os.path.join(BASE_PATH, "zhwiktionary-20190601-pages-meta-current.xml")

