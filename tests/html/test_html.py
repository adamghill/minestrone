import re

# Test that `HTML` is imported from the astrisk
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
