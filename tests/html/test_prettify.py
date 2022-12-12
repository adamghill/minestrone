from minestrone import HTML


def eq(actual, expected):
    print(expected)
    print("===")
    print(actual)

    assert actual == expected


def test_html_prettify_no_root():
    expected = """<li>
  <a class="sister" href="https://dormouse.com/elsie" id="elsie">Elsie</a>
</li>
<li>
  <a class="sister" href="https://dormouse.com/lacie" id="lacie">Lacie</a>
</li>
<li>
  <a class="sister" href="https://dormouse.com/tillie" id="tillie">Tillie</a>
</li>
"""

    html = HTML(
        """
<li>
<a class="sister" href="https://dormouse.com/elsie" id="elsie">Elsie</a>
</li>
<li>
<a class="sister" href="https://dormouse.com/lacie" id="lacie">Lacie</a>
</li>
<li>
<a class="sister" href="https://dormouse.com/tillie" id="tillie">Tillie</a>
</li>
"""
    )
    actual = html.prettify()

    eq(actual, expected)


def test_html_prettify_minimal():
    expected = """<ul>
  <li>
    <a class="sister" href="https://dormouse.com/elsie" id="elsie">Elsie</a>
  </li>
  <li>
    <a class="sister" href="https://dormouse.com/lacie" id="lacie">Lacie</a>
  </li>
  <li>
    <a class="sister" href="https://dormouse.com/tillie" id="tillie">Tillie</a>
  </li>
</ul>
"""

    html = HTML(
        """
<ul>
<li>
<a class="sister" href="https://dormouse.com/elsie" id="elsie">Elsie</a>
</li>
<li>
<a class="sister" href="https://dormouse.com/lacie" id="lacie">Lacie</a>
</li>
<li>
<a class="sister" href="https://dormouse.com/tillie" id="tillie">Tillie</a>
</li>
</ul>
"""
    )
    actual = html.prettify()

    eq(actual, expected)


def test_html_prettify_4_space_indent():
    expected = """<ul>
    <li>
        <a class="sister" href="https://dormouse.com/elsie" id="elsie">Elsie</a>
    </li>
    <li>
        <a class="sister" href="https://dormouse.com/lacie" id="lacie">Lacie</a>
    </li>
    <li>
        <a class="sister" href="https://dormouse.com/tillie" id="tillie">Tillie</a>
    </li>
</ul>
"""

    html = HTML(
        """
<ul>
<li>
<a class="sister" href="https://dormouse.com/elsie" id="elsie">Elsie</a>
</li>
<li>
<a class="sister" href="https://dormouse.com/lacie" id="lacie">Lacie</a>
</li>
<li>
<a class="sister" href="https://dormouse.com/tillie" id="tillie">Tillie</a>
</li>
</ul>
"""
    )
    actual = html.prettify(indent=4)

    eq(actual, expected)


def test_html_prettify_longlines():
    expected = """<ul>
  <li>
    <a class="sister" href="#" id="long-tweet">
      Voluptatum qui magni omnis molestias beatae sint dolor eius aliquid aut consequatur. Possimus optio dolores veniam voluptatibus autem iste ut et ut nostrum tempora quia facere. Reprehenderit at aut laboriosam consequatur id nulla.
    </a>
  </li>
</ul>
"""

    html = HTML(
        '<ul><li><a class="sister" href="#" id="long-tweet">Voluptatum qui magni omnis molestias beatae sint dolor eius aliquid aut consequatur. Possimus optio dolores veniam voluptatibus autem iste ut et ut nostrum tempora quia facere. Reprehenderit at aut laboriosam consequatur id nulla.</a></li></ul>'
    )
    actual = html.prettify()

    eq(actual, expected)


def test_html_prettify_longlines_none_max_line_length():
    expected = """<ul>
  <li>
    <a class="sister" href="#" id="long-tweet">Voluptatum qui magni omnis molestias beatae sint dolor eius aliquid aut consequatur. Possimus optio dolores veniam voluptatibus autem iste ut et ut nostrum tempora quia facere. Reprehenderit at aut laboriosam consequatur id nulla.</a>
  </li>
</ul>
"""

    html = HTML(
        '<ul><li><a class="sister" href="#" id="long-tweet">Voluptatum qui magni omnis molestias beatae sint dolor eius aliquid aut consequatur. Possimus optio dolores veniam voluptatibus autem iste ut et ut nostrum tempora quia facere. Reprehenderit at aut laboriosam consequatur id nulla.</a></li></ul>'
    )
    actual = html.prettify(max_line_length=None)

    eq(actual, expected)


def test_html_prettify_with_text_children():
    expected = """<ul>
  <li>
    extra text
    <a class="sister" href="#" id="long-tweet">Voluptatum qui</a>
    even more text
  </li>
</ul>
"""

    html = HTML(
        '<ul><li>extra text<a class="sister" href="#" id="long-tweet">Voluptatum qui</a>even more text</li></ul>'
    )
    actual = html.prettify()

    eq(actual, expected)


def test_html_prettify_with_text_children_2():
    expected = """<ul>
  <li>
    extra text1
    <a class="sister" href="#" id="long-tweet1">Voluptatum qui1</a>
    even more text1
  </li>
  <li>
    extra text2
    <a class="sister" href="#" id="long-tweet2">Voluptatum qui2</a>
    even more text2
  </li>
</ul>
"""

    html = HTML(
        """
<ul>
<li>extra text1<a class="sister" href="#" id="long-tweet1">Voluptatum qui1</a>even more text1</li>
<li>extra text2<a class="sister" href="#" id="long-tweet2">Voluptatum qui2</a>even more text2</li>
</ul>"""
    )
    actual = html.prettify()

    eq(actual, expected)


def test_html_prettify_with_text_children_3():
    expected = """<a>Voluptatum qui1</a>
1
<a>Voluptatum qui2</a>
"""

    html = HTML(
        """
<a>Voluptatum qui1</a>1
<a>Voluptatum qui2</a>
"""
    )
    actual = html.prettify()

    eq(actual, expected)


def test_html_prettify_with_text_children_4():
    expected = """9
<ul>
  <li>
    0
    1
    <a>Voluptatum qui1</a>
    2
    3
    <a>Voluptatum qui2</a>
    4
    <a>Voluptatum qui3</a>
    5
    6
    <a>Voluptatum qui4</a>
    7
  </li>
</ul>
8
"""

    html = HTML(
        """
9<ul>
<li>0
1<a>Voluptatum qui1</a>2
3<a>Voluptatum qui2</a>4
<a>Voluptatum qui3</a>5
6<a>Voluptatum qui4</a>
7</li>
</ul>8
"""
    )
    actual = html.prettify()

    eq(actual, expected)


def test_html_doc_prettify(html_doc):
    expected = """<html>
  <head>
    <title>The Dormouse's story</title>
  </head>
  <body>
    <h1>The Dormouse's story</h1>
    <ul>
      <li>
        <a href="https://dormouse.com/elsie" class="sister" id="elsie">Elsie</a>
      </li>
      <li>
        <a href="https://dormouse.com/lacie" class="sister" id="lacie">Lacie</a>
      </li>
      <li>
        <a href="https://dormouse.com/tillie" class="sister" id="tillie">Tillie</a>
      </li>
    </ul>
  </body>
</html>
"""

    actual = html_doc.prettify()

    eq(actual, expected)


def test_html_prettify_doc_example():
    expected = """<html>
  <head>
    <title>The Dormouse's Story</title>
  </head>
  <body>
    <h1>The Dormouse's Story</h1>
    <ul>
      <li>
        <a href="http://example.com/elsie" class="sister" id="elsie">Elsie</a>
      </li>
      <li>
        <a href="http://example.com/lacie" class="sister" id="lacie">Lacie</a>
      </li>
    </ul>
  </body>
</html>
"""

    html = HTML(
        """
<html>
<head>
<title>The Dormouse's Story</title>
</head>
<body>
<h1>The Dormouse's Story</h1>

<ul>
<li><a href="http://example.com/elsie" class="sister" id="elsie">Elsie</a></li>
<li><a href="http://example.com/lacie" class="sister" id="lacie">Lacie</a></li>
</ul>
</body>
</html>
"""
    )
    actual = html.prettify()

    eq(actual, expected)


def test_html_prettify_doc_example_2():
    expected = """<ul>
  <li id="li-1">1</li>
</ul>
"""

    html = HTML(
        """
<ul>
<li id="li-1">1</li>
</ul>"""
    )
    ul_element = next(html.query("ul"))
    actual = ul_element.prettify()
    print(actual)

    assert actual == expected
