"""
minestrone - Search, modify, and parse messy HTML with ease.
"""

from enum import Enum
from typing import Iterator, List, Optional, Union

import bs4

from .element import Element, Text
from .formatter import UnsortedAttributes

__all__ = [
    "HTML",
    "Element",
    "Text",
    "Parser",
]


class Parser(Enum):
    HTML = "html.parser"
    LXML = "lxml"
    HTML5 = "html5lib"


class HTML:
    encoding = "utf-8"

    def __init__(
        self,
        html: Union[str, "HTML"],
        parser: Parser = Parser.HTML,
        encoding: str = None,
    ):
        if isinstance(html, str) or isinstance(html, bytes):
            self._soup = bs4.BeautifulSoup(
                html, features=parser.value, from_encoding=encoding
            )
        elif isinstance(html, HTML):
            self._soup = html._soup
        else:
            raise Exception("Unknown type to init HTML")

        if encoding:
            self.encoding = encoding
        else:
            self.encoding = self._soup.original_encoding

    def query(self, selector: str) -> Iterator[Element]:
        """
        Returns an iterator of `Element`s that match the CSS selector.
        """

        for _tag in self._soup.select(selector):
            yield Element.convert_from_tag(self._soup, _tag)

    def query_to_list(self, selector: str) -> List[Element]:
        """
        Returns a list of `Element`s that match the CSS selector.
        """

        return list(self.query(selector))

    def prettify(
        self, indent: int = 2, max_line_length: int = 88, use_bs4: bool = False
    ) -> str:
        """
        Prettify HTML.

        Args:
            indent: How many spaces to indent for each level in the hierarchy. Defaults to 2.
            max_line_length: How long the line can reach before indenting another level. Defaults to 88. If `None` it will never used.
            use_bs4: Whether to use the `BeautifulSoup` `prettify` function or `minestrone`. Defaults to `False`.
        """

        if use_bs4:
            return self._soup.prettify()

        string = ""

        for top_level_child in self._soup.contents:
            if isinstance(top_level_child, bs4.element.Tag):
                element = Element.convert_from_tag(self._soup, top_level_child)
                string += element.prettify(indent, max_line_length)
            elif isinstance(top_level_child, str) and top_level_child != "\n":
                string += top_level_child.strip() + "\n"

        return string

    @property
    def root_element(self) -> Optional[Element]:
        """
        Gets the root `Element` for the HTML.
        """

        for _element in self._soup.contents:
            if isinstance(_element, bs4.element.Tag) and _element.name:
                return Element.convert_from_tag(self._soup, _element)

        return None

    def __str__(self):
        # Cleans up `beautifulsoup` modifications
        self._soup.smooth()

        # Prevents `beautifulsoup` from re-ordering attributes in alphabetical order
        return self._soup.encode(formatter=UnsortedAttributes()).decode()

    def __repr__(self):
        return self.__str__()
