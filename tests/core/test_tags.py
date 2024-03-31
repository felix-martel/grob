import re

from grob.core.parsers import CallableMultiPartParser, CallableParser, PatternParser
from grob.core.tags import DistributableTag, MultiPartTag, SinglePartTag, create_tags
from grob.types import KeyPart, OnMissing, TagName


def test_create_tag_with_pattern():
    (tag,) = create_tags("a/*/{b}.txt")
    assert tag == MultiPartTag(
        name=TagName("default"),
        parser=PatternParser("a/*/{b}.txt"),
    )


def test_create_tag_with_multiple_patterns():
    tag1, tag2 = create_tags({"t1": "a/{a}.txt", "t2": "b/{a}.txt"})
    assert tag1 == MultiPartTag(
        name=TagName("t1"),
        parser=PatternParser("a/{a}.txt"),
    )
    assert tag2 == MultiPartTag(
        name=TagName("t2"),
        parser=PatternParser("b/{a}.txt"),
    )


def test_create_tag_with_automatic_distribution():
    tag1, tag2 = create_tags({"t1": "{parent}/file-{i}.txt", "t2": "{parent}/label.txt"})
    assert tag1 == MultiPartTag(
        name=TagName("t1"),
        parser=PatternParser("{parent}/file-{i}.txt"),
    )
    assert tag2 == DistributableTag(
        name=TagName("t2"),
        parser=PatternParser("{parent}/label.txt"),
        distribute_over=[KeyPart("i")],
    )


def test_create_tag_with_options():
    (tag1,) = create_tags({"t1": {"spec": "{name}.*", "allow_multiple": True, "on_missing": "ignore"}})
    assert tag1 == MultiPartTag(
        name=TagName("t1"),
        parser=PatternParser("{name}.*"),
        allow_multiple=True,
        on_missing=OnMissing.ignore,
    )


def test_create_tag_with_compiled_regex():
    regex = re.compile(r"(?P<foo>.*)")
    (tag1,) = create_tags(regex)
    assert tag1.parser == PatternParser(regex)


def test_create_tag_with_regex():
    (tag1,) = create_tags("(?P<foo>.*):r")
    assert tag1.parser == PatternParser(re.compile("(?P<foo>.*)"))


def test_create_tag_with_callable():
    (tag1,) = create_tags(str)
    assert tag1 == SinglePartTag(name=TagName("default"), parser=CallableParser(str))


def test_create_tag_with_multipart_callable():
    split_dashes = lambda p: dict(zip(["a", "b"], str(p).split("-")))
    (tag1,) = create_tags({"tag1": {"spec": split_dashes, "key_parts": ["b", "a"]}})
    assert tag1 == MultiPartTag(
        name=TagName("tag1"),
        parser=CallableMultiPartParser(split_dashes, key_parts=["b", "a"]),
    )


# TODO: test failure paths
