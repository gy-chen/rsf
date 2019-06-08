import enum
import re
import logging
import xml.etree.ElementTree as ET
from opencc import OpenCC
from . import utils

logger = logging.getLogger()

cc = OpenCC("s2t")

PATTERN_RELATED_WORDS = re.compile(r"===相關詞彙===(.*)", re.DOTALL)
PATTERN_WORD = re.compile(r"\[\[(.*?)\]\]")


class _State(enum.Enum):
    PARSING_PAGE = enum.auto()
    OUTSIDE_PAGE = enum.auto()


class _Tag:
    PAGE = "{http://www.mediawiki.org/xml/export-0.10/}page"
    ID = "{http://www.mediawiki.org/xml/export-0.10/}id"
    TITLE = "{http://www.mediawiki.org/xml/export-0.10/}title"
    TEXT = "{http://www.mediawiki.org/xml/export-0.10/}text"


def parse(wiktionary_xml_path):
    """parse wiktionary XML

    Arguments:
        wiktionary_xml_path (str)

    Returns:
        list of dict in format {
            "id": id of the page,
            "title": "title of the page",
            "text": "content of the page",
        }
    """
    state = _State.OUTSIDE_PAGE
    current_page = None
    for event, elem in ET.iterparse(wiktionary_xml_path, ["start", "end"]):
        if event == "start":
            if elem.tag == _Tag.PAGE:
                if state != _State.OUTSIDE_PAGE:
                    raise ParsingError()
                current_page = {"id": None, "title": None, "text": None}
                state = _State.PARSING_PAGE
            else:
                logger.debug("ignore uninteresting start event element {}".format(elem))
        elif event == "end":
            if not state == _State.PARSING_PAGE:
                logger.debug(
                    "ignore element {} because not in parsing page state.".format(elem)
                )
                continue
            if elem.tag == _Tag.TITLE:
                current_page["title"] = elem.text
            elif elem.tag == _Tag.ID:
                try:
                    current_page["id"] = int(elem.text)
                except (ValueError, TypeError):
                    logger.warning("failed to convert elem id to int {}".format(elem))
            elif elem.tag == _Tag.TEXT:
                current_page["text"] = elem.text
            elif elem.tag == _Tag.PAGE:
                yield current_page
                state = _State.OUTSIDE_PAGE
                current_page = None
            else:
                logger.debug("ignore uninteresting end event elment {}".format(elem))


def parse_word(page):
    """parse word from page content

    Arguments:
        page (dict): in format {
            "id": id of the page,
            "title": "title of the page",
            "text": "content of the page",
        }

    Raises:
        ParsingError: if the page is not a word page

    Returns:
        dict in format {
            "word": "word name",
            "related": ["related word", ...]
        }
    """
    if page["title"] is None or page["text"] is None:
        raise ParsingError()
    word = cc.convert(page["title"])
    related_words_content = PATTERN_RELATED_WORDS.search(page["text"])
    if not related_words_content:
        raise ParsingError()
    related_words_content = related_words_content.group(1)
    words = _apply_filter(PATTERN_WORD.findall(related_words_content))
    if not words:
        raise ParsingError()
    return {"word": word, "related": words}


def _apply_filter(words):
    filter_chain = [
        utils.filter_exclude_punctuation,
        utils.filter_exclude_empty,
        _filter_to_traditional_chinese,
    ]
    for c in filter_chain:
        words = c(words)
    return list(words)


def _filter_to_traditional_chinese(words):
    for word in words:
        yield cc.convert(word)


class ParsingError(Exception):
    pass

