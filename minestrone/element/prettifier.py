import bs4

from . import Element


def prettify_element(
    element: Element,
    indent: int,
    max_line_length: int,
    spaces: str = "",
) -> str:
    def __increase_spaces(_spaces):
        return " " * (len(_spaces) + indent)

    def __decrease_spaces(_spaces):
        return " " * (len(_spaces) - indent)

    string = f"\n{spaces}{element.tag_string}"

    has_children = False

    content_children = [
        c
        for c in element._self.contents
        if (isinstance(c, str) and c != "\n") or isinstance(c, bs4.element.Tag)
    ]
    children = list(element.children)

    if content_children and children:
        for child in content_children.copy():
            if isinstance(child, str):
                string += child
                content_children.pop(0)
            else:
                break

    for child in children:
        if has_children is False:
            # Only increase the number of space for the first child
            spaces = __increase_spaces(spaces)

        content_children.pop(0)
        has_children = True
        string += prettify_element(child, indent, max_line_length, spaces=spaces)

    if content_children and children:
        for child in content_children:
            string += child

    if has_children:
        spaces = __decrease_spaces(spaces)
        string = f"{string}\n{spaces}{element.closing_tag_string}"
    else:
        is_long_line = False

        if max_line_length is not None and len(element._self.text) > max_line_length:
            is_long_line = True

        if is_long_line:
            spaces = __increase_spaces(spaces)
            string = f"{string}\n{spaces}"

        string = f"{string}{element._self.text}"

        if is_long_line:
            spaces = __decrease_spaces(spaces)
            string = f"{string}\n{spaces}"

        string = f"{string}{element.closing_tag_string}"

    return string
