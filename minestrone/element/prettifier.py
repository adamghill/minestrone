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

    string = f"{spaces}{element.tag_string}"

    content_children = [
        c
        for c in element._self.contents
        if (isinstance(c, str) and c != "\n") or isinstance(c, bs4.element.Tag)
    ]
    children = list(element.children)
    has_children = False

    if content_children and children:
        extra_child_spaces = __increase_spaces(spaces)

        for child in content_children.copy():
            content_children.pop(0)

            if isinstance(child, str):
                child_text = child.strip()

                # Make sure that any newlines are indented to the correct number of spaces
                child_text = child_text.replace("\n", f"\n{extra_child_spaces}")

                string = f"{string}\n{extra_child_spaces}{child_text}"
            else:
                break

    for child in children:
        if has_children is False:
            # Only increase the number of space for the first child
            spaces = __increase_spaces(spaces)

        if not string.endswith("\n"):
            string = f"{string}\n"

        has_children = True
        string += prettify_element(child, indent, max_line_length, spaces=spaces)

        if content_children and children:
            extra_child_spaces = __increase_spaces(spaces)

            for child in content_children.copy():
                content_children.pop(0)

                if isinstance(child, str):
                    child_text = child.strip()

                    # Make sure that any newlines are indented to the correct number of spaces
                    child_text = child_text.replace("\n", f"\n{spaces}")

                    string = f"{string}{spaces}{child_text}"
                else:
                    break

    if has_children:
        spaces = __decrease_spaces(spaces)

        if not string.endswith("\n"):
            string = f"{string}\n"

        string = f"{string}{spaces}{element.closing_tag_string}"
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

    if not string.endswith("\n"):
        string = f"{string}\n"

    return string
