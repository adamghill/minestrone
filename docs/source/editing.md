# Editing

To edit HTML, first query for an `Element` and then call one of the following methods.

## prepend

Adds new text or an element **before** the calling element.

### Prepend an element

```python
from minestrone import HTML
html = HTML("<span>Dormouse</span>")
html.root_element.prepend(name="span", text="The", klass="mr-2")

assert str(html) == "<span class="mr-2">The</span><span>Dormouse</span>"
```

### Prepend text

```python
from minestrone import HTML
html = HTML("<span>Dormouse</span>")
html.root_element.prepend(text="The ")

assert html == "The <span>Dormouse</span>"
```

## append

Adds text content or a new element **after** the calling element.

### Append an element

```python
from minestrone import HTML
html = HTML("<span>Dormouse</span>")
html.root_element.append(name="span", text="Story", klass="ml-2")

assert str(html) == "<span>Dormouse</span><span class="ml-2">Story</span>"
```

### Append text

```python
from minestrone import HTML
html = HTML("<span>Dormouse</span>")
html.root_element.append(text=" Story")

assert html == "<span>Dormouse</span> Story"
```
