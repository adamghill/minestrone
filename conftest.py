from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from minestrone import HTML


@pytest.fixture
def html_doc(html_doc_str) -> "HTML":
    from minestrone import HTML

    return HTML(html_doc_str)


@pytest.fixture
def html_doc_str() -> str:
    with open("tests/samples/html_doc.html", "r") as f:
        return f.read()


@pytest.fixture
def html_fragment(html_fragment_str) -> "HTML":
    from minestrone import HTML

    return HTML(html_fragment_str)


@pytest.fixture
def html_fragment_str() -> str:
    with open("tests/samples/html_fragment.html", "r") as f:
        return f.read()


@pytest.fixture
def html_unicorn_fragment(html_unicorn_fragment_str) -> "HTML":
    from minestrone import HTML

    return HTML(html_unicorn_fragment_str)


@pytest.fixture
def html_unicorn_fragment_str() -> str:
    with open("tests/samples/html_unicorn_fragment.html", "r") as f:
        return f.read()
