# Run this with `poe t tests/test_benchmarks.py --benchmark-only`
import re
from html.parser import HTMLParser
from typing import Iterator

from minestrone import HTML, Element

UNICORN_MODEL_REGEX = re.compile(
    r"(unicorn:model|u:model)(\.[^=]+)?=[\"'](?P<unicorn_model_name>[^\"']+)[\"']"
)

HTML_FRAGMENT = """<div unicorn:id="c5bFzZQZ" unicorn:name="wizard/wizard" unicorn:key="" unicorn:checksum="jAjZYLHS" unicorn:data="{}" unicorn:calls="[]">
    <div unicorn:calls="[]" unicorn:checksum="Nwb6p5BN" unicorn:data="{&quot;address&quot;:&quot;123 Main St&quot;,&quot;city&quot;:&quot;Anytown&quot;,&quot;state&quot;:&quot;CA&quot;,&quot;zip_code&quot;:&quot;12345&quot;}" unicorn:id="step2" unicorn:key="" unicorn:name="wizard/step2">
    <div>Step 2</div>
    <div>
    <input u:model.defer="address">
    <input u:model.lazy="city">
    <input u:model='state'>
    <input u:model="zip_code">
    </div>
    <div>
        Address: 123 Main St<br>
        City: Anytown<br>
        State: CA<br>
        Zip code: 12345<br>
    </div>
    <button unicorn:click="$parent.previous()">Previous</button>
    <button unicorn:click="$parent.next()">Next</button>
    </div>
    </div>"""

EXPECTED = ["address", "city", "state", "zip_code"]


def test_regex(benchmark):
    def _():
        return [
            m.group("unicorn_model_name")
            for m in UNICORN_MODEL_REGEX.finditer(HTML_FRAGMENT)
        ]

    actual = benchmark(_)
    assert EXPECTED == actual


def _minestrone_get_unicorn_models(element: Element) -> Iterator[str]:
    for attribute in element.attributes.keys():
        if attribute.startswith("unicorn:model") or attribute.startswith("u:model"):
            yield element.attributes[attribute]


def test_minestrone(benchmark):
    def _():
        minestrone_html = HTML(HTML_FRAGMENT)
        unicorn_model_names = []

        for element in minestrone_html.elements:
            for attribute_value in _minestrone_get_unicorn_models(element):
                unicorn_model_names.append(attribute_value)

        return unicorn_model_names

    actual = benchmark(_)
    assert EXPECTED == actual


def test_minestrone_with_existing_html(benchmark):
    minestrone_html = HTML(HTML_FRAGMENT)

    def _():
        unicorn_model_names = []

        for element in minestrone_html.elements:
            for attribute_value in _minestrone_get_unicorn_models(element):
                unicorn_model_names.append(attribute_value)

        return unicorn_model_names

    actual = benchmark(_)
    assert EXPECTED == actual


# def test_parsel(benchmark):
#     from parsel import Selector

#     def _():
#         selector = Selector(HTML_FRAGMENT)
#         unicorn_model_names = []

#         for element in selector.xpath("//*"):
#             for root_attr_name, root_attr_value in element.root.attrib.items():
#                 if root_attr_name.startswith(
#                     "unicorn:model"
#                 ) or root_attr_name.startswith("u:model"):
#                     unicorn_model_names.append(root_attr_value)
#         return unicorn_model_names

#     actual = benchmark(_)
#     assert EXPECTED == actual


def test_selectolax(benchmark):
    from selectolax.lexbor import LexborHTMLParser

    def _():
        parser = LexborHTMLParser(HTML_FRAGMENT)
        unicorn_model_names = []

        for node in parser.css("*"):
            for attr_name, attr_value in node.attributes.items():
                if attr_name.startswith("unicorn:model") or attr_name.startswith(
                    "u:model"
                ):
                    unicorn_model_names.append(attr_value)
        return unicorn_model_names

    actual = benchmark(_)
    assert EXPECTED == actual


# def test_markupever(benchmark):
#     import markupever  # type: ignore[unresolved-import]

#     def _():
#         doc = markupever.parse(HTML_FRAGMENT)
#         unicorn_model_names = []

#         for element in doc.root().descendants():
#             if isinstance(element, markupever.dom.Element):
#                 for key in element.attrs:
#                     attr_name = key.local
#                     if attr_name.startswith("unicorn:model") or attr_name.startswith(
#                         "u:model"
#                     ):
#                         unicorn_model_names.append(element.attrs.get(key))
#         return unicorn_model_names

#     actual = benchmark(_)
#     assert EXPECTED == actual


class UnicornModelParser(HTMLParser):
    def feed(self, data):
        self.unicorn_model_names = []

        super().reset()
        super().feed(data)

    def handle_starttag(self, tag, attrs: list):
        for attr in attrs:
            if attr[0].startswith("unicorn:model") or attr[0].startswith("u:model"):
                self.unicorn_model_names.append(attr[1])


def test_html_parser(benchmark):
    def _():
        parser = UnicornModelParser()
        parser.feed(HTML_FRAGMENT)

        return parser.unicorn_model_names

    actual = benchmark(_)
    assert EXPECTED == actual
