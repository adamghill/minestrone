import re

import pytest

# Test that `HTML` is imported from the asterisk
from minestrone import *


def test_html_str_unsorted_attributes(html_doc):
    with open("tests/samples/html_doc.html", "r") as f:
        original_html_doc = f.read()

    # All spaces are replaced which isn't great
    expected = original_html_doc
    expected = re.sub(r"^\s+", "", expected, flags=re.MULTILINE)
    actual = str(html_doc)

    assert actual == expected


def test_html_str_closes_tags():
    html = HTML(
        """<html>
  <head>
    <title>The Dormouse's story</title>
  </head>
  <body>
    <h1>The Dormouse's story</h1>"""
    )

    expected = """<html>
<head>
<title>The Dormouse's story</title>
</head>
<body>
<h1>The Dormouse's story</h1></body></html>"""

    actual = str(html)

    assert actual == expected


def test_html_fragments():
    html = HTML(
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
    html = HTML(html_fragment)

    assert str(html_fragment) == str(html)


def test_html_html_soups(html_fragment):
    html = HTML(html_fragment)

    assert html_fragment._soup == html._soup


def test_html_wrong_type():
    with pytest.raises(Exception):
        HTML(1)


def test_html_repr(html_fragment):
    assert repr(html_fragment) == str(html_fragment)


def test_html_parser_fragment(html_fragment_str):
    html_parsed_with_html = HTML(html_fragment_str, parser=Parser.HTML)
    assert html_parsed_with_html

    html_parsed_with_lxml = HTML(html_fragment_str, parser=Parser.LXML)
    assert html_parsed_with_lxml

    html_parsed_with_html5 = HTML(html_fragment_str, parser=Parser.HTML5)
    assert html_parsed_with_html5


def test_html_parser_fragment_html():
    assert str(HTML("<span>dormouse", parser=Parser.HTML)) == "<span>dormouse</span>"


def test_html_parser_fragment_lxml():
    assert (
        str(HTML("<span>dormouse", parser=Parser.LXML))
        == "<html><body><span>dormouse</span></body></html>"
    )


def test_html_parser_fragment_html5():
    assert (
        str(HTML("<span>dormouse", parser=Parser.HTML5))
        == "<html><head></head><body><span>dormouse</span></body></html>"
    )


def test_html_parser_doc(html_doc_str):
    html_parsed_with_html = HTML(html_doc_str, parser=Parser.HTML)
    assert html_parsed_with_html

    html_parsed_with_lxml = HTML(html_doc_str, parser=Parser.LXML)
    assert html_parsed_with_lxml

    html_parsed_with_html5 = HTML(html_doc_str, parser=Parser.HTML5)
    assert html_parsed_with_html5


def test_html_encoding():
    html = HTML(b"<h1>\xed\xe5\xec\xf9</h1>")
    assert str(html) == "<h1>翴檛</h1>"
    assert html.encoding == "big5"

    html = HTML(b"<h1>\xed\xe5\xec\xf9</h1>", encoding="iso-8859-8")
    assert str(html) == "<h1>םולש</h1>"
    assert html.encoding == "iso-8859-8"
