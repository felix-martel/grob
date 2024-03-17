import dataclasses
import re
from typing import Any, Callable, Dict, Iterable, List, Union

from grob.core import parsers
from grob.types import GroupKey, KeyPart, OnMissing, TagName, TagSpec

DEFAULT_TAG_NAME = TagName("default")


@dataclasses.dataclass
class Tag:
    name: TagName
    parser: parsers.Parser
    on_missing: OnMissing = OnMissing.fail
    allow_multiple: bool = False


@dataclasses.dataclass
class MultiPartTag(Tag):
    parser: parsers.MultiPartParserProtocol = None

    # This is an awful hack to allow default values on the parent class `Tag`. This won't be needed once we stop
    # supporting Python <3.10, since 3.10 introduces a `kw_only` argument
    def __post_init__(self):
        if self.parser is None:
            # TODO: error message
            raise ValueError(self)


@dataclasses.dataclass
class DistributableTag(MultiPartTag):
    distribute_over: List[KeyPart] = None

    def __post_init__(self):
        if self.distribute_over is None:
            raise ValueError(self)


@dataclasses.dataclass
class SinglePartTag(Tag):
    parser: parsers.SinglePartParserProtocol = None

    def __post_init__(self):
        if self.parser is None:
            raise ValueError(self)


def create_tags(
    raw_specs: Union[TagSpec, Dict[str, TagSpec]],
    key_formatter: Union[str, Callable[[parsers.MultiPartKey], GroupKey], None] = None,
) -> List[Tag]:
    specs = _normalize_spec(raw_specs)
    # Use a dict to preserve insertion order
    all_key_parts = list(
        {key_part: None for spec in specs.values() for key_part in getattr(spec["parser"], "key_parts", [])}
    )
    tags = [create_tag(name, **spec, all_key_parts=all_key_parts) for name, spec in specs.items()]
    return tags


def create_tag(
    name: str,
    parser: parsers.Parser,
    all_key_parts: List[KeyPart],
    allow_multiple: bool = False,
    on_missing: OnMissing = OnMissing.fail,
    distribute: bool = False,
    distribute_over: Iterable[str] = (),
) -> Tag:
    common_arguments = {
        "name": TagName(name),
        "parser": parser,
        "on_missing": on_missing,
        "allow_multiple": allow_multiple,
    }
    if isinstance(parser, parsers.CallableParser):
        return SinglePartTag(**common_arguments)
    elif (missing_key_parts := set(all_key_parts) - set(parser.key_parts)) or distribute:
        if not isinstance(parser, (parsers.PatternParser, parsers.CallableMultiPartParser)):
            # TODO: error message
            raise TypeError(parser)
        if not distribute_over:
            # Distribute over all keys that are not present in the pattern
            distribute_over = missing_key_parts
        return DistributableTag(
            **common_arguments,
            distribute_over=list(distribute_over),
        )
    else:
        return MultiPartTag(**common_arguments)


def _normalize_spec(spec: Union[TagSpec, Dict[str, TagSpec]]) -> Dict[TagName, Dict[str, Any]]:
    # Any is not actually Any, it's a TypedDict with a mandatory parser and optional keys
    if isinstance(spec, (str, re.Pattern)) or callable(spec):
        spec = {DEFAULT_TAG_NAME: spec}
    normalized_spec = {}
    for raw_tag_name, raw_tag_spec in spec.items():
        if isinstance(raw_tag_spec, (str, re.Pattern)) or callable(raw_tag_spec):
            raw_tag_spec = {"spec": raw_tag_spec}
        elif not isinstance(raw_tag_spec, dict):
            # TODO: error message
            raise TypeError(raw_tag_spec)
        elif "spec" not in raw_tag_spec:
            # TODO: error message
            raise ValueError(raw_tag_spec)
        parser_spec = raw_tag_spec.pop("spec")
        if isinstance(parser_spec, (str, re.Pattern)):
            parser = parsers.PatternParser(parser_spec)
        elif not callable(parser_spec):
            # TODO: error message
            raise TypeError(parser_spec)
        elif (key_parts := raw_tag_spec.pop("key_parts", None)) is not None:
            parser = parsers.CallableMultiPartParser(parser_spec, key_parts=key_parts)
        else:
            parser = parsers.CallableParser(parser_spec)
        if "on_missing" in raw_tag_spec:
            raw_tag_spec["on_missing"] = OnMissing(raw_tag_spec["on_missing"])
        normalized_spec[TagName(raw_tag_name)] = {"parser": parser, **raw_tag_spec}
    return normalized_spec
