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

    def __append_newline_if_needed(_strings):
        if not _strings[-1].endswith("\n"):
            _strings.append("\n")

    strings = []
    strings.append(spaces)
    strings.append(element.tag_string)

    content_children = [
        c
        for c in element._self.contents
        if (isinstance(c, str) and c != "\n") or isinstance(c, bs4.element.Tag)
    ]
    has_children = False

    for child in element.children:
        if has_children is False:
            if content_children:
                extra_child_spaces = __increase_spaces(spaces)

                for content_child in content_children.copy():
                    content_children.pop(0)

                    if isinstance(content_child, str):
                        child_text = content_child.strip()

                        if child_text:
                            # Make sure that any newlines are indented to the correct number of spaces
                            child_text = child_text.replace(
                                "\n", f"\n{extra_child_spaces}"
                            )

                            strings.append("\n")
                            strings.append(extra_child_spaces)
                            strings.append(child_text)
                    else:
                        break

            # Only increase the number of space for the first child
            spaces = __increase_spaces(spaces)

        __append_newline_if_needed(strings)

        has_children = True
        strings.append(prettify_element(child, indent, max_line_length, spaces=spaces))

        if content_children:
            extra_child_spaces = __increase_spaces(spaces)

            for child in content_children.copy():
                content_children.pop(0)

                if isinstance(child, str):
                    child_text = child.strip()

                    if child_text:
                        # Make sure that any newlines are indented to the correct number of spaces
                        child_text = child_text.replace("\n", f"\n{spaces}")

                        strings.append(spaces)
                        strings.append(child_text)
                else:
                    break

    if has_children:
        spaces = __decrease_spaces(spaces)

        __append_newline_if_needed(strings)
        strings.append(spaces)
        strings.append(element.closing_tag_string)
    else:
        is_long_line = False

        if max_line_length is not None and len(element._self.text) > max_line_length:
            is_long_line = True

        if is_long_line:
            spaces = __increase_spaces(spaces)
            strings.append("\n")
            strings.append(spaces)

        strings.append(element._self.text)

        if is_long_line:
            spaces = __decrease_spaces(spaces)
            strings.append("\n")
            strings.append(spaces)

        strings.append(element.closing_tag_string)

    __append_newline_if_needed(strings)

    return "".join(strings)
