import pytest

from minestrone import Element


def test_query_id(html_doc):
    elements = list(html_doc.query("a#elsie"))
    assert len(elements) == 1
    assert isinstance(elements[0], Element)

    expected = (
        '<a href="https://dormouse.com/elsie" class="sister" id="elsie">Elsie</a>'
    )
    actual = elements[0]

    assert str(actual) == expected


def test_query_class(html_doc):
    assert 3 == len(list(html_doc.query("a.sister")))


def test_query_tag(html_doc):
    assert 3 == len(list(html_doc.query("a")))


def test_elements_with_one_parent(html_unicorn_fragment):
    actual = len(list(html_unicorn_fragment.elements))
    expected = 15

    assert actual == expected


def test_elements_with_multiple_parents():
    from minestrone import HTML

    html = HTML(
        """
    <div></div>
    <span>Dormouse</span>
    """
    )

    assert [e.name for e in html.elements] == ["div", "span"]


def test_query_len_raises(html_doc):
    with pytest.raises(TypeError) as e:
        len(html_doc.query("a"))

    assert e.exconly() == "TypeError: object of type 'generator' has no len()"


def test_query_to_list(html_doc):
    assert 3 == len(html_doc.query_to_list("a"))


def test_query_css_selector(html_doc):
    for a in html_doc.query("ul li a.sister"):
        assert (
            str(a)
            == '<a href="https://dormouse.com/elsie" class="sister" id="elsie">Elsie</a>'
        )
        break
