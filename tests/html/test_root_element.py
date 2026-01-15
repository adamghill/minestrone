import pytest

from minestrone import HTML, Element


def test_root_element(html_doc):
    root_element = html_doc.root_element
    assert isinstance(root_element, Element)
    assert root_element.name == "html"


def test_root_element_with_extra_linebreaks():
    html = HTML(
        """

<p class="title"><b>The Dormouse's story</b></p>
    """
    )

    root_element = html.root_element
    assert isinstance(root_element, Element)
    assert root_element.name == "p"


def test_root_element_with_comment():
    html = HTML(
        """
<!-- -->
<p class="title"><b>The Dormouse's story</b></p>
    """
    )

    root_element = html.root_element
    assert isinstance(root_element, Element)
    assert root_element.name == "p"


def test_root_element_missing():
    html = HTML(
        """
<!-- -->
testing
    """
    )

    root_element = html.root_element
    assert root_element is None


@pytest.mark.parametrize(
    "tag_name, html_str",
    [
        ("meta", '<meta charset="utf-8">'),
        ("title", "<title>Test Title</title>"),
        ("style", "<style>body { color: red; }</style>"),
        ("base", '<base href="/">'),
        ("script", '<script>console.log("foo")</script>'),
    ],
)
def test_root_element_head_tags(tag_name, html_str):
    """Test elements that are implicitly moved to the head."""
    html = HTML(html_str)
    root = html.root_element
    assert isinstance(root, Element), f"Failed for {tag_name}"
    assert root.name == tag_name


def test_root_element_li():
    """Test list item element which is valid in body."""
    html = HTML("<li>Item</li>")
    root = html.root_element
    assert isinstance(root, Element)
    assert root.name == "li"


def test_root_element_hoisted_from_table():
    """Test element that is hoisted out of a table (foster parenting)."""
    # div is not allowed directly in table, so it gets hoisted before the table
    html = HTML("<table><div>foo</div></table>")

    # We expect the div to be the first element, so it becomes the root_element
    root = html.root_element
    assert isinstance(root, Element)
    assert root.name == "div"
