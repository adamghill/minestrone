from abc import ABC
from typing import Dict, Generator, List, Optional, Sequence, Union

import bs4

from ..formatter import UnsortedAttributes

# List of void elements from: https://www.thoughtco.com/html-singleton-tags-3468620
VOID_ELEMENTS = set(
    (
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
    )
)
HTML5_CLOSING_TAG = ""
XHTML_CLOSING_TAG = "/>"  # TODO: Be able to set XHTML mode


class Content(ABC):
    """Base class for `Text` and `Element` classes."""

    _soup: bs4.BeautifulSoup
    _self: Union[bs4.element.PageElement, bs4.element.Tag, bs4.element.Tag]

    def append(
        self, name: Optional[str] = None, text: Optional[str] = None, **kwargs
    ) -> Union["Element", "Text"]:
        """Adds `Text` or a new `Element` after the current `Element`.

        Args:
            name: The tag name of the new `Element` or `None` for `Text`.
            text: The text content either by itself or within the element, e.g. "test"
                would be the text for `<span>test</span>`.
            kwargs: Any attributes that should be added to the new element. Use "css"
                or "klass" for "class"; use the value of `True` for attributes that
                do not require a value like `disabled`. `None` for `Text`.

        Returns:
            The newly added `Element` or `Text`.
        """

        if name is None:
            assert text is not None, "Text content is required"
            assert not kwargs, "No attributes can be set for text content"

            self._self.insert_after(text)

            # Get the just inserted text
            next_sibling = self._self.next_sibling

            if next_sibling is not None and isinstance(
                next_sibling, bs4.element.NavigableString
            ):
                return Text.convert_from_navigable_string(self._soup, next_sibling)

            raise Exception("Could not find text")
        else:
            tag = self._create_tag(name, text=text, **kwargs)
            self._self.insert_after(tag)

            return Element.convert_from_tag(self._soup, tag)

    def prepend(self, name=None, text=None, **kwargs) -> Union["Element", "Text"]:
        """Adds a new element before the current element.

        Args:
            name: The name of the element.
            text: The `text content` of the element, e.g. "test" is the text for
                `<span>test</span>`
            kwargs: Any attributes that should be added to the new element. Use "css"
                or "klass" for "class"; use the value of `True` for attributes that
                do not require a value like `disabled`.

        Returns:
            The newly created element or `None` if text content was prepended.
        """

        if name is None:
            assert text is not None, "Text content is required"
            assert not kwargs, "No attributes can be set for text content"

            self._self.insert_before(text)

            # Get the just inserted text
            previous_sibling = self._self.previous_sibling

            if previous_sibling is not None and isinstance(
                previous_sibling, bs4.element.NavigableString
            ):
                return Text.convert_from_navigable_string(self._soup, previous_sibling)

            raise Exception("Could not find text")
        else:
            tag = self._create_tag(name, text=text, **kwargs)
            self._self.insert_before(tag)

            return Element.convert_from_tag(self._soup, tag)

    def _create_tag(self, name, text=None, **kwargs) -> bs4.element.Tag:
        """Creates a new bs4 tag to be inserted."""

        attrs = self._convert_attributes(kwargs)

        tag = self._soup.new_tag(name, attrs=attrs)

        if text:
            tag.string = text

        return tag

    def _convert_attributes(self, attributes: Dict) -> Dict:
        """Converts the attributes dictionary. Handles "klass"/"css" to "class" conversion.
        Also handles a value of `True` for attributes like `disabled`.

        Returns:
            A new dictionary.
        """

        attrs = {}

        for key, value in attributes.items():
            if key == "klass" or key == "css":
                key = "class"

            if value is True:
                value = key

            attrs[key] = value

        return attrs


class Text(Content):
    _self: bs4.element.NavigableString

    @staticmethod
    def convert_from_navigable_string(
        soup: bs4.BeautifulSoup,
        navigable_string: bs4.element.NavigableString,
    ) -> "Text":
        text = Text()
        text._soup = soup
        text._self = navigable_string

        return text

    def __str__(self):
        return str(self._self)

    def __repr__(self):
        return self.__str__()


class Element(Content):
    _self: bs4.element.Tag

    @staticmethod
    def create(
        name: str, text: str = None, soup: bs4.BeautifulSoup = None, **kwargs
    ) -> "Element":
        """Create the `Element`."""

        element = Element()

        if soup is None:
            soup = bs4.BeautifulSoup()

        element._soup = soup

        tag = element._create_tag(name, text=text, **kwargs)
        element._self = tag

        return element

    @staticmethod
    def convert_from_tag(soup: bs4.BeautifulSoup, tag: bs4.element.Tag) -> "Element":
        """Gets the name of the `Element`."""

        element = Element()
        element._soup = soup
        element._self = tag

        return element

    @property
    def name(self) -> str:
        """Gets the name of the `Element`."""

        return self._self.name

    @property
    def id(self) -> Optional[str]:
        """Gets the id of the `Element`."""

        return self._self.attrs.get("id")

    @id.setter
    def id(self, string: str) -> None:
        """Sets the `id` of the `Element`."""

        self._self.attrs["id"] = string.__class__(string)

    @property
    def attributes(self) -> Dict:
        """Attributes of the `Element`."""

        attrs = {}

        for k, v in self._self.attrs.items():
            if k == "class":
                attrs["class"] = " ".join(v)
            else:
                attrs[k] = v

        return attrs

    @attributes.setter
    def attributes(self, value: Dict):
        attrs = self._convert_attributes(value)

        for k, v in attrs.items():
            if k == "class":
                if isinstance(v, str):
                    attrs[k] = v.split(" ")
                elif isinstance(v, Sequence):
                    attrs[k] = list(v)
                else:
                    raise Exception("Invalid type for CSS classes")

        self._self.attrs = attrs

    @property
    def classes(self) -> List[str]:
        """Return all classes of the element."""

        return list(self._self.attrs.get("class", []))

    @property
    def children(self) -> Generator["Element", None, None]:
        """Returns an iterator of `Element`s of the children of the element."""

        for child in self._self.children:
            if isinstance(child, bs4.element.Tag):
                yield Element.convert_from_tag(self._soup, child)

    @property
    def parent(self) -> Optional["Element"]:
        """Returns the parent `Element` of the element."""

        if self._self.parent:
            return Element.convert_from_tag(self._soup, self._self.parent)

        return None

    @property
    def text(self) -> Optional[str]:
        """Gets the `text content` of the element.

        For example:
        `<span>Hello World</span>` would return "Hello World"

        `<h1><code>Hello</code> World</h1>` would return "<code>Hello</code> World"
        """

        return "".join([str(c) for c in self._self.contents])

    @property
    def tag_string(self) -> str:
        _attributes = self.attributes.items()

        if not _attributes:
            return f"<{self.name}>"

        _tag_string = f"<{self.name}"

        for key, value in _attributes:
            if isinstance(value, list):
                value = " ".join(value)

            _tag_string += f' {key}="{value}"'

        _tag_string = f"{_tag_string}>"

        return _tag_string

    @property
    def closing_tag_string(self) -> str:
        if self._self.is_empty_element or self.name in VOID_ELEMENTS:
            return HTML5_CLOSING_TAG

        return f"</{self.name}>"

    @text.setter
    def text(self, string: str) -> None:
        """Sets the `text content` of the element."""

        self._self.clear()
        self._self.append(string.__class__(string))

    def prettify(self, indent: int = 2, max_line_length: int = 88):
        # Import here to avoid circular imports
        from .prettifier import prettify_element

        return prettify_element(self, indent, max_line_length)

    def __str__(self):
        return self._self.encode(formatter=UnsortedAttributes()).decode()

    def __repr__(self):
        return self.__str__()
