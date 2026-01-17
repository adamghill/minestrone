# Querying

`minestrone` allows searching through HTML via CSS selectors (similar to jQuery or other frontend libraries).

## root_element

Gets the root [element](element.md) of the HTML.

```python
from minestrone import HTML
html = HTML("""
<div>
  <span>Dormouse</span>
</div>
""")

assert html.root_element.name == "div"
```

## elements

Recursively get all [elements](element.md) in the HTML.

```python
from minestrone import HTML
html = HTML("""
<div>
  <span>Dormouse</span>
</div>
""")

assert [e.name for e in html.elements] == ["div", "span"]
```

## query

Takes a CSS selector and returns an iterator of [`Element`](element.md) items.

### Query by element name

```python
from minestrone import HTML
html = HTML("""
<h1>The Dormouse's Story</h1>
<p>There was a table...</p>
""")

for h1 in html.query("h1"):
    assert str(h1) == "<h1>The Dormouse's Story</h1>"
```

### Query by id

```python
from minestrone import HTML
html = HTML("""
<ul>
  <li><a href="http://example.com/elsie" class="sister" id="elsie">Elsie</a></li>
  <li><a href="http://example.com/lacie" class="sister" id="lacie">Lacie</a></li>
</ul>
""")

for a in html.query("a#elsie"):
    assert str(a) == '<a href="http://example.com/elsie" class="sister" id="elsie">Elsie</a>'
```

### Query by class

```python
from minestrone import HTML
html = HTML("""
<ul>
  <li><a href="http://example.com/elsie" class="sister" id="elsie">Elsie</a></li>
  <li><a href="http://example.com/lacie" class="sister" id="lacie">Lacie</a></li>
</ul>
""")

elsie_link = next(html.query("ul li a.sister"))
assert str(elsie_link) == '<a href="http://example.com/elsie" class="sister" id="elsie">Elsie</a>'

lacie_link = next(html.query("ul li a.sister"))
assert str(lacie_link) == '<a href="http://example.com/lacie" class="sister" id="lacie">Lacie</a>'
```

## query_to_list

Exactly the same as [query](querying.md#query) except it returns a list of [`Element`](element.md) items instead of a generator. This is sometimes more useful than the `query` above, but it can take more time to parse and more memory to store the data if the HTML document is large.

```python
from minestrone import HTML
html = HTML("""
<ul>
  <li><a href="http://example.com/elsie" class="sister" id="elsie">Elsie</a></li>
  <li><a href="http://example.com/lacie" class="sister" id="lacie">Lacie</a></li>
</ul>
""")

assert len(html.query_to_list("a")) == 2
assert str(html.query_to_list("a")[0]) == '<a href="http://example.com/elsie" class="sister" id="elsie">Elsie</a>'
assert html.query_to_list("a") == list(html.query("a"))
```
