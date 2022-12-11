# Parsing

The `HTML` class parses a string of HTML and provides methods to [query](querying.md) the DOM for specific elements.

## \_\_init\_\_

Creates an `HTML` object from a `str` or `bytes`.

```python
from minestrone import HTML
html = HTML("""
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
""")
```

If closing tags are missing, then they will be added as needed to make the HTML valid.

```python
from minestrone import HTML
assert str(HTML("<span>dormouse")) == "<span>dormouse</span>"
```

### parser
Three parsers are available in `minestrone` and they all have different trade-offs. By default, the built-in, pure Python `html.parser` is used. `lxml` can be used for faster parsing speed. `html5lib` is another option to ensure a valid HTML5 document.

```{note}
`lxml` and `html5lib` are not installed with `minestrone` by default and must be specifically installed.

- `poetry add minestrone[lxml]` or `pip install minestrone[lxml]`
- `poetry add minestrone[html5]` or `pip install minestrone[html5]`
```

```{note}
BeautifulSoup has a [summary table](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser) of the three parsers. There is also a more detailed [breakdown of the differences](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#differences-between-parsers) between the parsers.
```

### Parser.HTML

```python
from minestrone import HTML, Parser
assert str(HTML("<span>dormouse"), parser=Parser.HTML) == "<span>dormouse</span>"
```

### Parser.LXML

```python
from minestrone import HTML, Parser
assert str(HTML("<span>dormouse"), parser=Parser.LXML) == "<html><body><span>dormouse</span></body></html>"
```

### Parser.HTML5

```python
from minestrone import HTML, Parser
assert str(HTML("<span>dormouse"), parser=Parser.HTML5) == "<html><head></head><body><span>dormouse</span></body></html>"
```

## encoding

`Beautiful Soup` [attempts to decipher the encoding](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#encodings) of the HTML string, however it isn't always correct. An encoding can be passed along if necessary.

```python
from minestrone import HTML, Parser
html_bytes = b"<h1>\xed\xe5\xec\xf9</h1>"

assert str(HTML(html_bytes)) == "<h1>翴檛</h1>"
assert HTML(html_bytes).encoding == "big5"

assert str(HTML(html_bytes), encoding="iso-8859-8") == "<h1>םולש</h1>"
assert HTML(html_bytes).encoding == "iso-8859-8"
```

## prettify

Returns a prettified version of the HTML.

```python
html = HTML("""
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
""")

assert html.prettify() == """
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
</html>"""
```


## \_\_str\_\_

Returns the `HTML` object as a string.

```python
from minestrone import HTML
html = HTML("""
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
""")

assert str(html) == """<html>
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
</html>"""
```

```{note}
Rendering the `HTML` into a string _will_ remove preceding spaces.
```
