import pytest

from ledes_parser import get_parser
from ledes_parser.ledes_parser import (
    SUPPORTED_SPECS,
    UnrecognizedLEDESVersionError,
    UnsupportedLEDESVersionError,
)


def test_get_parser_unrecognized_spec_raises_unrecognized_error():
    with pytest.raises(
        UnrecognizedLEDESVersionError, match=r"not a known LEDES specification"
    ):
        get_parser(spec="a goose")


def test_get_parser_unsupported_spec_raises_version_error():
    with pytest.raises(UnsupportedLEDESVersionError, match=r"has not been written yet"):
        get_parser(spec="LEDES98BI")


def test_get_parser_with_supported_spec():
    for spec in SUPPORTED_SPECS:
        try:
            parser = get_parser(spec=spec)
            assert parser is not None
        except Exception:
            pytest.fail(
                f"get_parser should have returned a parser for spec '{spec}' but raised an error instead."
            )
