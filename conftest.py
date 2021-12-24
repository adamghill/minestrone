import pytest

from minestrone import HTML


@pytest.fixture
def html_doc() -> HTML:
    with open("tests/samples/html_doc.html", "r") as f:
        return HTML(f.read())


@pytest.fixture
def html_fragment() -> HTML:
    with open("tests/samples/html_fragment.html", "r") as f:
        return HTML(f.read())
