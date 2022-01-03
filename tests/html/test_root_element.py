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
