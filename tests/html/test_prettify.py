import time

import pytest

from minestrone import HTML

PRINT_TIMINGS = True


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

    eq(actual, expected)


def test_hacker_news():
    expected = """<html op="news">
  <head>
    <meta name="referrer" content="origin">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="news.css?zR7cuBLVYytByk2yBoUd">
    <link rel="shortcut icon" href="favicon.ico">
    <link rel="alternate" type="application/rss+xml" title="RSS" href="rss">
    <title>Hacker News</title>
  </head>
  <body>
    <center>
      <table id="hnmain" border="0" cellpadding="0" cellspacing="0" width="85%" bgcolor="#f6f6ef">
        <tbody>
          <tr>
            <td bgcolor="#ff6600">
              <table border="0" cellpadding="0" cellspacing="0" width="100%" style="padding:2px">
                <tbody>
                  <tr>
                    <td style="width:18px;padding-right:4px">
                      <a href="https://news.ycombinator.com">
                        <img src="y18.gif" width="18" height="18" style="border:1px white solid;">
                      </a>
                    </td>
                    <td style="line-height:12pt; height:10px;">
                      <span class="pagetop">
                        <b class="hnname">
                          <a href="news">Hacker News</a>
                        </b>
                        <a href="newest">new</a>
                        |
                        <a href="front">past</a>
                        |
                        <a href="newcomments">comments</a>
                        |
                        <a href="ask">ask</a>
                        |
                        <a href="show">show</a>
                        |
                        <a href="jobs">jobs</a>
                        |
                        <a href="submit">submit</a>
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </td>
          </tr>
        </tbody>
      </table>
    </center>
  </body>
</html>
"""

    html = HTML(
        """
    <html op="news"><head><meta name="referrer" content="origin"><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" type="text/css" href="news.css?zR7cuBLVYytByk2yBoUd">
  <link rel="shortcut icon" href="favicon.ico">
    <link rel="alternate" type="application/rss+xml" title="RSS" href="rss">
  <title>Hacker News</title></head><body><center><table id="hnmain" border="0" cellpadding="0" cellspacing="0" width="85%" bgcolor="#f6f6ef">
  <tr><td bgcolor="#ff6600"><table border="0" cellpadding="0" cellspacing="0" width="100%" style="padding:2px"><tr><td style="width:18px;padding-right:4px"><a href="https://news.ycombinator.com"><img src="y18.gif" width="18" height="18" style="border:1px white solid;"></a></td>
            <td style="line-height:12pt; height:10px;"><span class="pagetop"><b class="hnname"><a href="news">Hacker News</a></b>
        <a href="newest">new</a> | <a href="front">past</a> | <a href="newcomments">comments</a> | <a href="ask">ask</a> | <a href="show">show</a> | <a href="jobs">jobs</a> | <a href="submit">submit</a>            </span></td>
        </tr>
            </table>
          </td>
        </tr>
      </table>
    </center>
  </body>
</html>
"""
    )
    actual = html.prettify()

    eq(actual, expected)


def test_link_tags():
    expected = """<link rel="preconnect" href="https://avatars.githubusercontent.com">
<link crossorigin="anonymous" media="all" rel="stylesheet" href="https://github.githubassets.com/assets/light-719f1193e0c0.css">
<link data-color-theme="dark" crossorigin="anonymous" media="all" rel="stylesheet" data-href="https://github.githubassets.com/assets/dark-0c343b529849.css">
<link data-color-theme="dark_dimmed" crossorigin="anonymous" media="all" rel="stylesheet" data-href="https://github.githubassets.com/assets/dark_dimmed-f22da508b62a.css">
"""

    html = HTML(
        """<link rel="preconnect" href="https://avatars.githubusercontent.com">
<link crossorigin="anonymous" media="all" rel="stylesheet" href="https://github.githubassets.com/assets/light-719f1193e0c0.css" />
<link data-color-theme="dark" crossorigin="anonymous" media="all" rel="stylesheet" data-href="https://github.githubassets.com/assets/dark-0c343b529849.css" />
<link data-color-theme="dark_dimmed" crossorigin="anonymous" media="all" rel="stylesheet" data-href="https://github.githubassets.com/assets/dark_dimmed-f22da508b62a.css" />
    """
    )
    actual = html.prettify()

    eq(actual, expected)


def test_comments():
    expected = """<div>
  <link rel="preconnect" href="https://avatars.githubusercontent.com">
  <!-- some comment here -->
  <link data-color-theme="dark" crossorigin="anonymous" media="all" rel="stylesheet" data-href="https://github.githubassets.com/assets/dark-0c343b529849.css">
</div>
"""

    html = HTML(
        """<div><link rel="preconnect" href="https://avatars.githubusercontent.com">
<!-- some comment here -->
<link data-color-theme="dark" crossorigin="anonymous" media="all" rel="stylesheet" data-href="https://github.githubassets.com/assets/dark-0c343b529849.css" />
</div>
    """
    )
    actual = html.prettify()

    eq(actual, expected)

    expected = """<link rel="preconnect" href="https://avatars.githubusercontent.com">
<!-- some comment here -->
<link data-color-theme="dark" crossorigin="anonymous" media="all" rel="stylesheet" data-href="https://github.githubassets.com/assets/dark-0c343b529849.css">
"""

    html = HTML(
        """<link rel="preconnect" href="https://avatars.githubusercontent.com">
            <!-- some comment here -->
            <link data-color-theme="dark" crossorigin="anonymous" media="all" rel="stylesheet" data-href="https://github.githubassets.com/assets/dark-0c343b529849.css" />
    """
    )
    actual = html.prettify()

    eq(actual, expected)


@pytest.mark.parametrize(
    "name",
    [
        "hacker-news",
        "amazon",
        "bbc",
        "bing",
        "bootstrap",
        "coding-horror",
        "github",
        "google",
        "ny-times",
        "reddit",
        "stack-overflow",
        "twitter",
        "wikipedia",
        # "ecma-262",  # this takes a long time
    ],
)
def test_html_prettify_samples(name):
    with open(f"tests/html/samples/expected/{name}.html") as f:
        expected = f.read()

    with open(f"tests/html/samples/{name}.html") as f:
        html = f.read()

    start_time = time.time()
    actual = HTML(html).prettify()

    if PRINT_TIMINGS:
        elapsed_seconds = time.time() - start_time

        print(f"minestrone parse {name} took: {elapsed_seconds} seconds")

        if elapsed_seconds > 10:
            assert 0, f"{name} took longer than 10 seconds to prettify"

    # if expected == "":
    #     with open(f"tests/html/samples/expected/{name}.html", "w") as f:
    #         f.write(actual)

    eq(actual, expected)
