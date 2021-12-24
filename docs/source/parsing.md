# Parsing

The `HTML` class parses a string of HTML and provides methods to [query](querying.md) the DOM for specific elements.

## \_\_init\_\_

Creates an `HTML` object from a string.

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
