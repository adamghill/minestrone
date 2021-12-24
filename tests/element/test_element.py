from minestrone import Element


def test_get_text(html_doc):
    tillie = next(html_doc.query("a#tillie"))

    expected = "Tillie"
    actual = tillie.text

    assert actual == expected


def test_set_text(html_doc):
    tillie = next(html_doc.query("a#tillie"))

    tillie.text = "Billie"

    expected = "Billie"
    actual = tillie.text

    assert actual == expected


def test_get_name(html_doc):
    tillie = next(html_doc.query("a#tillie"))

    expected = "a"
    actual = tillie.name

    assert actual == expected


def test_element_klass():
    actual = Element.create("button", "Save", klass="test-class")

    expected = '<button class="test-class">Save</button>'

    assert str(actual) == expected


def test_element_get_attributes():
    span = Element.create(
        "span",
        "test attrs content",
        klass="test-class1 test-class2",
        disabled=True,
        id="span1",
    )

    assert span.name == "span"
    assert span.text == "test attrs content"
    assert span.attributes == {
        "class": "test-class1 test-class2",
        "disabled": "disabled",
        "id": "span1",
    }


def test_element_set_attributes_klass():
    span = Element.create(
        "span",
        klass="test-class1",
    )

    span.attributes = {"klass": "test-class2 test-class3"}

    assert span.name == "span"
    assert span.attributes == {
        "class": "test-class2 test-class3",
    }
    assert span.classes == ["test-class2", "test-class3"]


def test_element_set_attributes_css():
    span = Element.create(
        "span",
        klass="test-class1",
    )

    span.attributes = {"css": "test-class2 test-class3"}

    assert span.name == "span"
    assert span.attributes == {
        "class": "test-class2 test-class3",
    }
    assert span.classes == ["test-class2", "test-class3"]


def test_element_set_attributes_class():
    span = Element.create(
        "span",
        klass="test-class1",
    )

    span.attributes = {"class": "test-class2 test-class3"}

    assert span.name == "span"
    assert span.attributes == {
        "class": "test-class2 test-class3",
    }
    assert span.classes == ["test-class2", "test-class3"]


def test_element_classes_from_klass():
    span = Element.create(
        "span",
        klass="test-class1 test-class2",
    )

    assert span.classes == ["test-class1", "test-class2"]


def test_element_classes_from_css():
    span = Element.create(
        "span",
        css="test-class1 test-class2",
    )

    assert span.classes == ["test-class1", "test-class2"]
