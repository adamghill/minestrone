import pytest

# Test that `HTML` is imported from the asterisk
from minestrone import *  # noqa: F403


def test_html_str_unsorted_attributes(html_doc):
    actual = str(html_doc)

    # Check that attributes are preserved and not sorted (which is implied if it matches original mostly)
    # Original: <a href="https://dormouse.com/elsie" class="sister" id="elsie">Elsie</a>
    assert (
        '<a href="https://dormouse.com/elsie" class="sister" id="elsie">Elsie</a>'
        in actual
    )


def test_html_str_closes_tags():
    html = HTML(  # noqa: F405
        """<html>
  <head>
    <title>The Dormouse's story</title>
  </head>
  <body>
    <h1>The Dormouse's story</h1>"""
    )

    actual = str(html)

    # Selectolax normalizes structure tags (removing whitespace between some tags),
    # so we check that the essential tags and content are present.
    assert "<html><head>" in actual
    assert "<body>" in actual
    assert "<h1>The Dormouse's story</h1>" in actual
    assert "</html>" in actual


def test_html_fragments():
    html = HTML(  # noqa: F405
        """<h1>The Dormouse's story</h1>
    <ul>
      <li><a href="https://dormouse.com/elsie" class="sister" id="elsie">Elsie</a></li>
      <li><a href="https://dormouse.com/lacie" class="sister" id="lacie">Lacie</a></li>
      <li><a href="https://dormouse.com/tillie" class="sister" id="tillie">Tillie</a></li>
    </ul>"""
    )

    expected = """<h1>The Dormouse's story</h1>
    <ul>
      <li><a href="https://dormouse.com/elsie" class="sister" id="elsie">Elsie</a></li>
      <li><a href="https://dormouse.com/lacie" class="sister" id="lacie">Lacie</a></li>
      <li><a href="https://dormouse.com/tillie" class="sister" id="tillie">Tillie</a></li>
    </ul>"""

    actual = str(html)

    assert actual == expected


def test_html_html_strings(html_fragment):
    html = HTML(html_fragment)  # noqa: F405

    assert str(html_fragment) == str(html)


def test_html_wrong_type():
    with pytest.raises(Exception):
        HTML(1)  # type: ignore[invalid-argument-type] # noqa: F405


def test_html_repr(html_fragment):
    assert repr(html_fragment) == str(html_fragment)


def test_html_encoding():
    # Auto-detection is removed/not supported by Lexbor defaults
    # But we can test explicit encoding
    html = HTML(b"<h1>\xed\xe5\xec\xf9</h1>", encoding="big5")  # noqa: F405
    assert "<h1>翴檛</h1>" in str(html)

    html = HTML(b"<h1>\xed\xe5\xec\xf9</h1>", encoding="iso-8859-8")  # noqa: F405
    assert "<h1>םולש</h1>" in str(html)
    assert html.encoding == "iso-8859-8"
