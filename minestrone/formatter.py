import bs4


class UnsortedAttributes(bs4.formatter.HTMLFormatter):
    """
    Prevent `beautifulsoup` from re-ordering HTML attributes.
    """

    def __init__(self):
        super().__init__(
            entity_substitution=bs4.dammit.EntitySubstitution.substitute_html
        )

    def attributes(self, tag: bs4.element.Tag):
        for k, v in tag.attrs.items():
            yield k, v
