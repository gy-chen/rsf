"""provides functions for converting wiktionary export xml to mongo

this module simplify importing processing:
    - only import page element data
    - only choose first revision to store
"""
import logging
from . import parser
from . import config
from . import utils

logger = logging.getLogger()


def convert(storage, wiktionary_xml_path):
    """convert wiktionary xml to mongo db

    Arguments:
        storage (rsf.storage.Storage)
        wiktionary_xml_path (str)
    """
    pages = parser.parse(wiktionary_xml_path)

    def parse_word(pages):
        for page in pages:
            try:
                word = parser.parse_word(page)
                logger.info("parsed word {}".format(word["word"]))
                yield word
            except parser.ParsingError:
                logger.debug(
                    "parsing error while parsing {}".format(page["title"])
                )
                continue

    words = parse_word(pages)
    storage.store_wiktionary_words(words)


def main_convert(config=config.ConvertConfig):
    logging.basicConfig(level=logging.INFO)
    storage = utils.get_storage(config.MONGO)
    convert(storage, config.WIKTIONARY_XML_PATH)
