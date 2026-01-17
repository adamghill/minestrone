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

## encoding

The encoding of the HTML string is detected automatically, however it isn't always correct. An encoding can be passed along if necessary.

```python
from minestrone import HTML
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

assert html.prettify() == """<html>
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
