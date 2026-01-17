# Changelog

## 0.9.0

- Switch to `selectolax` for parsing.

### Breaking Changes

- `HTML` no longer has a `parser` parameter.

## 0.8.0

- Add `Element.insert` and `Element.remove_children`.

## 0.7.0

- Add `HTML.elements`.

## 0.6.2

- Optimize `prettify` method to be as fast as possible.
- Support HTML doctype, comments, void elements, and other improvements for `prettify`.

## 0.6.1

- Fix a few bugs for `HTML.prettify()` and `Element.prettify()`.

## 0.6.0

- Add `Element.prettify()`.

## 0.5.1

- Handle HTML tags when getting `Element.text`.

## 0.5.0

- Add setter for `Element.id`.
