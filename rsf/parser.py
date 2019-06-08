import enum
import logging
import xml.etree.ElementTree as ET

logger = logging.getLogger()


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


class ParsingError(Exception):
    pass

