from typing import List, Optional

from minestrone.element import VOID_ELEMENTS, Element


def prettify_element(
    element: Element,
    indent: int,
    max_line_length: Optional[int],
    spaces: str = "",
) -> str:
    def __increase_spaces(_spaces: str) -> str:
        return " " * (len(_spaces) + indent)

    def __decrease_spaces(_spaces: str) -> str:
        return " " * (len(_spaces) - indent)

    def __append_newline_if_needed(_strings: List[str]) -> None:
        if _strings and not _strings[-1].endswith("\n"):
            _strings.append("\n")

    def __append_string(_strings: List[str], _string: Optional[str]) -> None:
        if _string:
            _strings.append(_string)

    strings = []
    __append_string(strings, spaces)
    __append_string(strings, element.tag_string)

    content_children = []

    # We access the raw node to traverse
    curr = element._node.child
    while curr:
        content_children.append(curr)
        curr = curr.next

    has_children = False

    child_elements = list(element.children)

    for child_element in child_elements:
        if has_children is False:
            if content_children:
                extra_child_spaces = __increase_spaces(spaces)

                for content_child in content_children.copy():
                    # Stop if we hit the current child element
                    if content_child.mem_id == child_element._node.mem_id:
                        break

                    content_children.pop(0)

                    if content_child.is_text_node:
                        child_text = content_child.text()
                        if child_text:
                            child_text = child_text.strip()

                        if child_text:
                            # Make sure that any newlines are indented to the correct number of spaces
                            child_text = child_text.replace(
                                "\n", f"\n{extra_child_spaces}"
                            )

                            __append_string(strings, "\n")
                            __append_string(strings, extra_child_spaces)
                            __append_string(strings, child_text)
                    elif content_child.is_comment_node:
                        __append_string(strings, "\n")
                        __append_string(strings, extra_child_spaces)
                        __append_string(
                            strings, f"<!-- {content_child.comment_content} -->"
                        )

            if element.name not in VOID_ELEMENTS:
                # Only increase the number of spaces if the current element can have children
                # and it's the first child
                spaces = __increase_spaces(spaces)

        __append_newline_if_needed(strings)

        has_children = True
        __append_string(
            strings,
            prettify_element(child_element, indent, max_line_length, spaces=spaces),
        )

        if (
            content_children
            and content_children[0].mem_id == child_element._node.mem_id
        ):
            content_children.pop(0)

        if content_children:
            extra_child_spaces = __increase_spaces(spaces)

            for child in content_children.copy():
                # Stop if we hit next element (not text/comment)
                if child.is_element_node:
                    break

                content_children.pop(0)

                if child.is_text_node:
                    child_text = child.text()
                    if child_text:
                        child_text = child_text.strip()

                    if child_text:
                        # Make sure that any newlines are indented to the correct number of spaces
                        child_text = child_text.replace("\n", f"\n{spaces}")
                        __append_string(strings, spaces)

                        __append_string(strings, child_text)

                elif child.is_comment_node:
                    __append_string(strings, spaces)
                    __append_string(strings, f"<!-- {child.comment_content} -->")

    if has_children:
        spaces = __decrease_spaces(spaces)

        __append_newline_if_needed(strings)
        __append_string(strings, spaces)
        __append_string(strings, element.closing_tag_string)
    else:
        is_long_line = False
        text_content = element.text or ""

        if max_line_length is not None and len(text_content) > max_line_length:
            is_long_line = True

        if is_long_line:
            spaces = __increase_spaces(spaces)
            __append_string(strings, "\n")
            __append_string(strings, spaces)

        for child in content_children:
            if child.is_text_node:
                __append_string(strings, child.text())
            elif child.is_comment_node:
                __append_string(strings, f"<!-- {child.comment_content} -->")
            elif child.is_element_node:
                pass

        if is_long_line:
            spaces = __decrease_spaces(spaces)
            __append_string(strings, "\n")
            __append_string(strings, spaces)

        __append_string(strings, element.closing_tag_string)

    __append_newline_if_needed(strings)

    return "".join(strings)
