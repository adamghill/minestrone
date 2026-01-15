"""Element and Text classes for minestrone."""

from typing import Dict, Iterator, List, Optional, Union

from selectolax.lexbor import LexborHTMLParser, LexborNode


class Content:
    """Base class for `Text` and `Element` classes."""

    _node: LexborNode

    def _convert_attributes(self, attributes: Dict) -> Dict:
        """Convert attributes to be compatible with `selectolax`."""
        new_attributes: Dict[str, str] = {}

        for k, v in attributes.items():
            if k == "class" or k == "klass" or k == "css":
                k = "class"

            if v is True:
                v = k

            new_attributes[k] = str(v)

        return new_attributes

    def append(
        self, name: Optional[str] = None, text: Optional[str] = None, **kwargs
    ) -> Union["Element", "Text"]:
        """Add `Text` or a new `Element` after the current `Element`."""
        if name is None:
            if text is None:
                raise ValueError("Text content is required")
            if kwargs:
                raise ValueError("No attributes can be set for text content")

            # selectolax does not have `insert_text_after`, so use `insert_after`
            self._node.insert_after(text)

            # Get the newly inserted text node
            next_node = self._node.next

            if next_node and next_node.is_text_node:
                return Text(next_node)

            raise Exception("Could not find inserted text node")
        else:
            element = Element.create(name, text, **kwargs)
            self._node.insert_after(element._node)
            inserted = self._node.next
            if not inserted:
                raise Exception("Could not find inserted element")
            return Element(inserted)

    def prepend(
        self, name: Optional[str] = None, text: Optional[str] = None, **kwargs
    ) -> Union["Element", "Text"]:
        """Add a new element before the current element."""
        if name is None:
            if text is None:
                raise ValueError("Text content is required")
            if kwargs:
                raise ValueError("No attributes can be set for text content")

            self._node.insert_before(text)
            prev_node = self._node.prev
            if prev_node and prev_node.is_text_node:
                return Text(prev_node)
            raise Exception("Could not find inserted text node")
        else:
            element = Element.create(name, text, **kwargs)
            self._node.insert_before(element._node)
            inserted = self._node.prev
            if not inserted:
                raise Exception("Could not find inserted element")
            return Element(inserted)


class Text(Content):
    def __init__(self, node: LexborNode):
        """Initialize Text."""
        self._node = node

    def __str__(self) -> str:
        return self._node.text_content or ""

    def __repr__(self) -> str:
        return self.__str__()


class Element(Content):
    def __init__(self, node: LexborNode):
        """Initialize Element."""
        self._node = node

    @staticmethod
    def create(
        name: str,
        text: Optional[str] = None,
        **kwargs,
    ) -> "Element":
        """Create a detached `Element`."""
        html = f"<{name}></{name}>"
        parser = LexborHTMLParser(html)

        if not parser.body or not parser.body.child:
            raise Exception(f"Could not create element {name}")

        node = parser.body.child

        if text:
            node.insert_child(text)

        element = Element(node)

        # Apply attributes
        if kwargs:
            element.attributes = kwargs

        return element

    @property
    def name(self) -> str:
        """Get the tag name."""
        return self._node.tag or ""

    @property
    def id(self) -> Optional[str]:
        """Get the element id."""
        return self._node.attrs.get("id")

    @id.setter
    def id(self, value: str) -> None:
        """Set the element id."""
        self._node.attrs["id"] = value

    @property
    def attributes(self) -> Dict:
        """Get the element attributes."""
        return dict(self._node.attrs)

    @attributes.setter
    def attributes(self, value: Dict) -> None:
        """Set the element attributes."""
        for k in list(self._node.attrs.keys()):
            del self._node.attrs[k]

        for k, v in value.items():
            if k == "class" or k == "klass" or k == "css":
                k = "class"

            if isinstance(v, (list, tuple)):
                v = " ".join(v)

            if v is True:
                v = k

            if not isinstance(v, (str, bool, list, tuple)):
                raise ValueError(
                    f"Attribute value must be a string, boolean, list, or tuple, not {type(v)}"
                )

            self._node.attrs[k] = str(v)

    @property
    def classes(self) -> List[str]:
        """Get the element classes."""
        cls = self._node.attrs.get("class")
        if cls:
            return cls.split()
        return []

    @classes.setter
    def classes(self, value: List[str]) -> None:
        """Set the element classes."""
        self._node.attrs["class"] = " ".join(value)

    @property
    def children(self) -> Iterator["Element"]:
        """Get the child elements."""
        curr = self._node.child
        while curr:
            if curr.is_element_node:
                yield Element(curr)
            curr = curr.next

    @property
    def parent(self) -> Optional["Element"]:
        """Get the parent element."""
        p = self._node.parent
        if p:
            return Element(p)
        return None

    @property
    def text(self) -> str:
        """Get the text content."""
        texts = []
        curr = self._node.child
        while curr:
            if curr.is_text_node:
                texts.append(curr.text_content)
            else:
                texts.append(curr.html)
            curr = curr.next
        return "".join(texts)

    @text.setter
    def text(self, value: str) -> None:
        """Set the text content."""
        # Remove all children
        while self._node.child:
            self._node.child.remove()

        self._node.insert_child(value)

    @property
    def tag_string(self) -> str:
        """Get the opening tag string."""
        parts = [self.name]
        for k, v in self.attributes.items():
            parts.append(f'{k}="{v}"')
        return f"<{' '.join(parts)}>"

    @property
    def closing_tag_string(self) -> str:
        """Get the closing tag string."""
        if self.name in VOID_ELEMENTS:
            return ""
        return f"</{self.name}>"

    def insert(self, element: "Element", index: int = 0) -> None:
        """Insert a child element at the specified index."""
        if index < 0:
            self._node.insert_child(element._node)
            return

        curr = self._node.child
        if index == 0:
            if curr:
                curr.insert_before(element._node)
            else:
                self._node.insert_child(element._node)
            return

        i = 0
        while curr and i < index:
            curr = curr.next
            i += 1

        if curr:
            curr.insert_before(element._node)
        else:
            self._node.insert_child(element._node)

    def remove_children(self) -> None:
        """Remove all child elements."""
        while self._node.child:
            self._node.child.remove()

    def _create_tag(self, name: str, text: Optional[str] = None, **kwargs) -> "Element":
        """Create a new tag."""
        return Element.create(name, text, **kwargs)

    def prettify(self, indent: int = 2, max_line_length: Optional[int] = 88) -> str:
        """Prettify the element."""
        from minestrone.element.prettifier import prettify_element

        return prettify_element(self, indent, max_line_length)

    def __str__(self) -> str:
        return self._node.html or ""

    def __repr__(self) -> str:
        return self.__str__()


VOID_ELEMENTS = {
    "area",
    "base",
    "br",
    "col",
    "command",
    "embed",
    "hr",
    "img",
    "input",
    "keygen",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}
