from minestrone import HTML, Text


def test_create_tag_with_true_attribute_value(html_fragment: HTML):
    elsie = next(html_fragment.query("a#elsie"))
    actual = elsie._create_tag("button", "Save", disabled=True)

    expected = '<button disabled="disabled">Save</button>'

    assert str(actual) == expected


def test_create_tag_with_klass(html_fragment: HTML):
    elsie = next(html_fragment.query("a#elsie"))
    actual = elsie._create_tag("button", "Save", klass="test-class")

    expected = '<button class="test-class">Save</button>'

    assert str(actual) == expected


def test_prepend(html_fragment: HTML):
    elsie = next(html_fragment.query("a#elsie"))
    elsie.prepend("span", "test prepend content", klass="test-class")

    expected = """<ul>
  <li><span class="test-class">test prepend content</span><a href="https://dormouse.com/elsie" class="sister" id="elsie">Elsie</a></li>
  <li><a href="https://dormouse.com/lacie" class="sister" id="lacie">Lacie</a></li>
  <li><a href="https://dormouse.com/tillie" class="sister" id="tillie">Tillie</a></li>
</ul>"""

    actual = str(html_fragment)

    assert actual == expected


def test_text_str(html_fragment: HTML):
    elsie = next(html_fragment.query("a#elsie"))
    text = elsie.prepend(text="test prepend text content")

    expected = "test prepend text content"
    actual = str(text)

    assert actual == expected


def test_text_repr(html_fragment: HTML):
    elsie = next(html_fragment.query("a#elsie"))
    text = elsie.prepend(text="test prepend text content")

    expected = "test prepend text content"
    actual = repr(text)

    assert actual == expected


def test_prepend_text(html_fragment: HTML):
    elsie = next(html_fragment.query("a#elsie"))
    elsie.prepend(text="test prepend text content")

    expected = """<ul>
  <li>test prepend text content<a href="https://dormouse.com/elsie" class="sister" id="elsie">Elsie</a></li>
  <li><a href="https://dormouse.com/lacie" class="sister" id="lacie">Lacie</a></li>
  <li><a href="https://dormouse.com/tillie" class="sister" id="tillie">Tillie</a></li>
</ul>"""

    actual = str(html_fragment)

    assert actual == expected


def test_append(html_fragment: HTML):
    elsie = next(html_fragment.query("a#elsie"))
    elsie.append("span", "test append content", klass="test-class")

    expected = """<ul>
  <li><a href="https://dormouse.com/elsie" class="sister" id="elsie">Elsie</a><span class="test-class">test append content</span></li>
  <li><a href="https://dormouse.com/lacie" class="sister" id="lacie">Lacie</a></li>
  <li><a href="https://dormouse.com/tillie" class="sister" id="tillie">Tillie</a></li>
</ul>"""

    actual = str(html_fragment)

    assert actual == expected


def test_append_text(html_fragment: HTML):
    elsie = next(html_fragment.query("a#elsie"))

    text = elsie.append(text="test append text content")
    assert text
    assert isinstance(text, Text)

    expected = """<ul>
  <li><a href="https://dormouse.com/elsie" class="sister" id="elsie">Elsie</a>test append text content</li>
  <li><a href="https://dormouse.com/lacie" class="sister" id="lacie">Lacie</a></li>
  <li><a href="https://dormouse.com/tillie" class="sister" id="tillie">Tillie</a></li>
</ul>"""

    actual = str(html_fragment)

    assert actual == expected


def test_append_text_to_text(html_fragment: HTML):
    elsie = next(html_fragment.query("a#elsie"))
    first_text = elsie.append(text="test append 1")
    assert first_text
    assert isinstance(first_text, Text)

    second_text = first_text.append(text=" test append 2")
    assert second_text
    assert isinstance(second_text, Text)

    expected = """<ul>
  <li><a href="https://dormouse.com/elsie" class="sister" id="elsie">Elsie</a>test append 1 test append 2</li>
  <li><a href="https://dormouse.com/lacie" class="sister" id="lacie">Lacie</a></li>
  <li><a href="https://dormouse.com/tillie" class="sister" id="tillie">Tillie</a></li>
</ul>"""

    actual = str(html_fragment)

    assert actual == expected


def test_append_multiple(html_fragment: HTML):
    elsie = next(html_fragment.query("a#elsie"))
    new_tag = elsie.append("span", "test append content 1", klass="test-class")
    new_tag.append("span", "test append content 2", klass="test-class")

    expected = """<ul>
  <li><a href="https://dormouse.com/elsie" class="sister" id="elsie">Elsie</a><span class="test-class">test append content 1</span><span class="test-class">test append content 2</span></li>
  <li><a href="https://dormouse.com/lacie" class="sister" id="lacie">Lacie</a></li>
  <li><a href="https://dormouse.com/tillie" class="sister" id="tillie">Tillie</a></li>
</ul>"""

    actual = str(html_fragment)

    assert actual == expected
