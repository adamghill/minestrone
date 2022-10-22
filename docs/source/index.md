# Introduction

`minestrone` is a opinionated Python library that lets you search, modify, and parse messy HTML with ease.

## Behind the scenes

`minestrone` utilizes [`Beautiful Soup`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to do all the real work, but aims to provide a simple, consistent, and intuitive API to interact with an HTML document. `Beautiful Soup` provides a _lot_ of functionality, although it can be hard to grok the documentation. The hope is that `minestrone` makes that functionality easier.

## Related projects

There are a few other libraries to interact with HTML in Python, but most are focused on the retrieval of HTML and searching through the document. However, they are listed below in case they might be useful.

### Beautiful Soup related

- [`SoupSieve`](https://facelessuser.github.io/soupsieve/): provides selecting, matching, and filtering using modern CSS selectors. It provides the functionality used by the `select` function in `Beautiful Soup` which is also used by `minestrone`, however it can be used separately.
- [`soupy`](https://soupy.readthedocs.io/): wrapper around `Beautiful Soup` that makes it easier to search through HTML and XML documents.
- [`fast-soup`](https://pypi.org/project/fast-soup/): faster `Beautiful Soup` search via `lxml`.
- [`BeautifulSauce`](https://github.com/nateraw/BeautifulSauce): `Beautiful Soup`'s saucy sibling!
- [`SoupCan`](https://pypi.org/project/soupcan/): simplifies the process of designing a Python tool for extracting and displaying webpage content.

### Beautiful Soup replacements

- [`gazpacho`](https://pypi.org/project/gazpacho/): simple, fast, and modern web scraping library. The library is stable, actively maintained, and installed with zero dependencies.
- [`Requests-HTML`](https://requests-html.kennethreitz.org/): HTML Parsing for Humans. It intends to make parsing HTML (e.g. scraping the web) as simple and intuitive as possible.

```{toctree}
:maxdepth: 2
:hidden:

self
installation
```

```{toctree}
:caption: HTML
:maxdepth: 2
:hidden:

parsing
querying
element
editing
```

```{toctree}
:maxdepth: 2
:hidden:

GitHub <https://github.com/adamghill/minestrone>
Sponsor <https://github.com/sponsors/adamghill>
```
