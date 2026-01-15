"""minestrone - Search, modify, and parse messy HTML with ease."""

import re
from typing import Iterator, List, Optional, Union

from selectolax.lexbor import LexborHTMLParser

from minestrone.element import Content, Element, Text

__all__ = [
    "HTML",
    "Content",
    "Element",
    "Text",
]


class HTML:
    encoding: Optional[str] = "utf-8"
    _input_is_fragment: bool = False
    html: str
    _parser: LexborHTMLParser

    def __init__(
        self,
        html: Union[str, bytes, "HTML"],
        encoding: Optional[str] = None,
    ) -> None:
        """Analyze, search, and modify HTML."""

        if isinstance(html, HTML):
            self.html = html.html
            self._parser = LexborHTMLParser(self.html)
            self._input_is_fragment = html._input_is_fragment
        elif isinstance(html, (str, bytes)):
            if isinstance(html, bytes):
                if encoding:
                    html = html.decode(encoding)
                else:
                    html = html.decode("utf-8")  # Default fallback

            self.html = html
            self._parser = LexborHTMLParser(html)

            self._input_is_fragment = self._is_fragment(html)
        else:
            raise Exception("Unknown type to initialize HTML")

        if encoding:
            self.encoding = encoding

    def query(self, selector: str) -> Iterator[Element]:
        """Return an iterator of `Element`s that match the CSS selector."""
        for node in self._parser.css(selector):
            yield Element(node)

    def query_to_list(self, selector: str) -> List[Element]:
        """Return a list of `Element`s that match the CSS selector."""
        return list(self.query(selector))

    def prettify(
        self,
        indent: int = 2,
        max_line_length: Optional[int] = 88,
    ) -> str:
        """Prettify HTML."""
        strings = []

        if self._input_is_fragment:
            # Iterate head and body children
            if self._parser.head:
                curr = self._parser.head.child

                while curr:
                    if curr.is_element_node:
                        element = Element(curr)
                        strings.append(element.prettify(indent, max_line_length))
                    elif curr.is_text_node:
                        text_content = curr.text_content
                        text = text_content.strip() if text_content else ""
                        if text:
                            strings.append(f"{text}\n")
                    elif curr.is_comment_node:
                        strings.append(f"<!-- {curr.comment_content} -->\n")

                    curr = curr.next

            if self._parser.body:
                curr = self._parser.body.child

                while curr:
                    if curr.is_element_node:
                        element = Element(curr)
                        strings.append(element.prettify(indent, max_line_length))
                    elif curr.is_text_node:
                        text_content = curr.text_content
                        text = text_content.strip() if text_content else ""
                        if text:
                            strings.append(f"{text}\n")
                    elif curr.is_comment_node:
                        strings.append(f"<!-- {curr.comment_content} -->\n")

                    curr = curr.next
        else:
            if self._parser.root and self._parser.root.parent:
                curr = self._parser.root.parent.child
            else:
                curr = None

            while curr:
                if curr.tag == "-doctype":
                    strings.append("<!DOCTYPE html>\n")
                elif curr.tag == "html":
                    element = Element(curr)
                    strings.append(element.prettify(indent, max_line_length))
                elif curr.is_comment_node:
                    strings.append(f"<!-- {curr.comment_content} -->\n")

                curr = curr.next

        return "".join(strings)

    @property
    def root_element(self) -> Optional[Element]:
        """Gets the root `Element` for the HTML."""
        if self._input_is_fragment:
            # Check head first (e.g. link, meta tags)
            if self._parser.head:
                curr = self._parser.head.child
                while curr:
                    if curr.is_element_node:
                        return Element(curr)
                    curr = curr.next

            # Check body
            if self._parser.body:
                curr = self._parser.body.child
                while curr:
                    if curr.is_element_node:
                        return Element(curr)
                    curr = curr.next

            return None

        if not self._parser.root:
            return None

        return Element(self._parser.root)

    @property
    def elements(self) -> Iterator[Element]:
        """Recursively yield all `Element`s in the HTML."""
        for node in self._parser.css("*"):
            if self._input_is_fragment and node.tag in ("html", "head", "body"):
                continue

            yield Element(node)

    def __str__(self) -> str:
        if self._input_is_fragment:
            return self._serialize_fragment()
        return self._parser.html or ""

    def _serialize_fragment(self) -> str:
        """Serialize as a fragment, skipping html/head/body wrappers."""
        output = []

        # Traverse Document children
        # If html node -> traverse its children (Head, Body)
        if self._parser.root and self._parser.root.parent:
            curr = self._parser.root.parent.child
        else:
            curr = None
        while curr:
            if curr.tag == "html":
                # Check head
                if self._parser.head:
                    head_child = self._parser.head.child
                    while head_child:
                        output.append(head_child.html)
                        head_child = head_child.next

                # Check body
                if self._parser.body:
                    body_child = self._parser.body.child
                    while body_child:
                        output.append(body_child.html)
                        body_child = body_child.next
            else:
                if curr.is_comment_node:
                    output.append(f"<!-- {curr.comment_content} -->")
                elif curr.tag == "-doctype":
                    output.append(curr.html)
                else:
                    output.append(curr.html)

            curr = curr.next

        return "".join(output)

    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def _is_fragment(html: str) -> bool:
        """Heuristic to detect if input is a fragment or full document."""
        # Create a working copy to strip content from to check for start
        text = html.lstrip()

        # Iteratively strip comments from the start
        while True:
            if text.startswith("<!--"):
                end_idx = text.find("-->")
                if end_idx != -1:
                    text = text[end_idx + 3 :].lstrip()
                    continue
            break

        if re.match(r"^<(html|body|!DOCTYPE)(?=(\s|>))", text, re.IGNORECASE):
            return False

        return True
