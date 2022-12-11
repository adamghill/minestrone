import bs4
import pytest

from minestrone import HTML, Element


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


def test_element_set_attributes_id():
    span = Element.create(
        "span",
    )

    assert span.id is None

    span.attributes = {"id": "test-id"}

    assert span.id == "test-id"
    assert span.attributes == {
        "id": "test-id",
    }


def test_element_set_id():
    span = Element.create(
        "span",
    )

    assert span.id is None

    span.id = "test-id"

    assert span.id == "test-id"
    assert span.attributes == {
        "id": "test-id",
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


def test_element_set_attributes_class_list():
    span = Element.create(
        "span",
        klass="test-class1",
    )

    span.attributes = {"css": ["test-class2", "test-class3"]}

    assert span.name == "span"
    assert span.attributes == {
        "class": "test-class2 test-class3",
    }
    assert span.classes == ["test-class2", "test-class3"]


def test_element_set_attributes_class_tuple():
    span = Element.create(
        "span",
        klass="test-class1",
    )

    span.attributes = {"css": ("test-class2", "test-class3")}

    assert span.name == "span"
    assert span.attributes == {
        "class": "test-class2 test-class3",
    }
    assert span.classes == ["test-class2", "test-class3"]


def test_element_set_attributes_invalid_type():
    span = Element.create("span")

    with pytest.raises(Exception):
        span.attributes = {"css": 0}


def test_element_classes_from_klass_kwarg():
    span = Element.create(
        "span",
        klass="test-class1 test-class2",
    )

    assert span.classes == ["test-class1", "test-class2"]


def test_element_classes_from_css_kwarg():
    span = Element.create(
        "span",
        css="test-class1 test-class2",
    )

    assert span.classes == ["test-class1", "test-class2"]


def test_element_classes_empty():
    span = Element.create("span")

    assert span.classes == []


def test_element_children(html_doc):
    ul = next(html_doc.query("ul"))

    assert len(list(ul.children)) == 3

    # get generator so next() will work to get all children
    children = ul.children

    first_li = next(children)
    elsie = next(first_li.children)
    assert elsie.id == "elsie"
    assert len(list(elsie.children)) == 0

    second_li = next(children)
    lacie = next(second_li.children)
    assert lacie.id == "lacie"

    third_li = next(children)
    tillie = next(third_li.children)
    assert tillie.id == "tillie"


def test_element_parent(html_doc):
    elsie = next(html_doc.query("#elsie"))

    assert elsie.parent
    assert elsie.parent.name == "li"
    assert elsie.parent.parent.name == "ul"


def test_element_parent_none(html_doc: HTML):
    assert html_doc.root_element
    assert html_doc.root_element.parent
    assert html_doc.root_element.parent.parent is None


def test_create_without_soup():
    span = Element.create(
        "span",
    )

    assert span._soup


def test_create_with_soup():
    soup = bs4.BeautifulSoup()

    span = Element.create(
        "span",
        soup=soup,
    )

    assert span._soup
    assert id(span._soup) == id(soup)


def test_repr():
    span = Element.create(
        "span",
    )

    assert repr(span) == "<span></span>"
