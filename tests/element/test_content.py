import pytest

from minestrone.element import Content


@pytest.fixture
def content():
    return Content()


def test_convert_attributes_klass(content):
    attributes = {"klass": "test1"}
    actual = content._convert_attributes(attributes)

    assert actual == {"class": "test1"}


def test_convert_attributes_css(content):
    attributes = {"css": "test1"}
    actual = content._convert_attributes(attributes)

    assert actual == {"class": "test1"}


def test_convert_attributes_true_value(content):
    attributes = {"disabled": True}
    actual = content._convert_attributes(attributes)

    assert actual == {"disabled": "disabled"}
