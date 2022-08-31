# Element

`Element`s are returned from [querying](querying.md) methods. They have the following properties to retrieve their data.

## name

Gets the name of the `Element`.

```python
html = HTML("<span>Dormouse</span>")
span_element = html.root_element

assert span_element.name == "span"
```

## id

Gets the id of the `Element`.

```python
html = HTML("<span id='dormouse'>Dormouse</span>")
span_element = html.root_element

assert span_element.id == "dormouse"
```

## attributes

### Get attributes

```python
html = HTML("<button class="mt-2 pb-2" disabled>Wake up</button>")
button_element = html.root_element

assert button_element.attributes == {"class": "mt-2 pb-2", "disabled": True}
```

### Set attributes

```python
html = HTML("<button>Go back to sleep</button>")
button_element = html.root_element
button_element.attributes = {"class": "mt-2 pb-2", "disabled": True}

assert str(button_element) == '<button class="mt-2 pb-2" disabled>Go back to sleep</button>'
```

## classes

Gets a list of classes for the element.

```python
html = HTML("<button class="mt-2 pb-2">Wake Up</button>")
button_element = html.root_element

assert button_element.classes == ["mt-2", "pb-2"]
```

## text

### Get text context

```python
html = HTML("<button>Wake Up</button>")
button_element = html.root_element

assert button_element.text == "Wake Up"
```

### Set text content

```python
html = HTML("<button>Wake Up</button>")
button_element = html.root_element

button_element.text = "Go back to sleep"

assert str(button_element) == "<button>Go back to sleep</button>"
```

## children

Gets an iterator of the children for the element.

```python
html = HTML("""
<ul>
    <li>1</li>
    <li>2</li>
    <li>3</li>
</ul>
""")
ul_element = html.root_element

assert len(list(ul_element.children)) == 3
```

## parent

Gets the parent for the element.

```python
html = HTML("""
<ul>
    <li id="li-1">1</li>
</ul>
""")
li_element = html.query("#li-1")

assert li_element.parent.name == "ul"
```
