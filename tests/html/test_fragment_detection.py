from minestrone import HTML


def test_full_document_standard():
    html_str = "<html><body>Full</body></html>"
    html = HTML(html_str)
    assert html._input_is_fragment is False


def test_full_document_whitespace():
    html_str = "   <html><body>Whitespace Full</body></html>"
    html = HTML(html_str)
    assert html._input_is_fragment is False


def test_full_document_doctype():
    html_str = "<!DOCTYPE html><html></html>"
    html = HTML(html_str)
    assert html._input_is_fragment is False


def test_full_document_doctype_case_insensitive():
    html_str = "<!doctype html><html></html>"
    html = HTML(html_str)
    assert html._input_is_fragment is False


def test_full_document_body_only():
    html_str = "<BODY>Content</BODY>"
    html = HTML(html_str)
    assert html._input_is_fragment is False


def test_full_document_with_leading_comment():
    html_str = "<!-- comment --><html><body>Full</body></html>"
    html = HTML(html_str)
    assert html._input_is_fragment is False


def test_full_document_with_multiple_leading_comments():
    html_str = "<!-- c1 --> <!-- c2 --> <html><body>Full</body></html>"
    html = HTML(html_str)
    assert html._input_is_fragment is False


def test_full_document_with_multiline_leading_comment():
    html_str = """<!-- 
       multiline 
       comment 
    --> <html>Full</html>"""
    html = HTML(html_str)
    assert html._input_is_fragment is False


def test_fragment_simple_div():
    html_str = "<div>Simple fragment</div>"
    html = HTML(html_str)
    assert html._input_is_fragment is True


def test_fragment_commented_out_html_tag():
    html_str = "<!-- <html> --><div>Commented out root tag</div>"
    html = HTML(html_str)
    assert html._input_is_fragment is True


def test_fragment_commented_out_html_tag_wrapped():
    html_str = "<div><!-- <html> --></div>"
    html = HTML(html_str)
    assert html._input_is_fragment is True


def test_fragment_script_containing_html_string():
    html_str = "<script>var s = '<html>';</script>"
    html = HTML(html_str)
    assert html._input_is_fragment is True


def test_fragment_custom_html_tag():
    html_str = "<html-custom>Custom tag</html-custom>"
    html = HTML(html_str)
    assert html._input_is_fragment is True


def test_fragment_custom_body_tag():
    html_str = "<body-custom>Custom tag</body-custom>"
    html = HTML(html_str)
    assert html._input_is_fragment is True
