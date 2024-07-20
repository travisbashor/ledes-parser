import pytest

from ledes_parser import get_parser
from ledes_parser.ledes_parser import (
    SUPPORTED_SPECS,
    UnrecognizedLEDESVersionError,
    UnsupportedLEDESVersionError,
)


def test_get_parser_with_unsupported_spec():
    with pytest.raises(
        UnrecognizedLEDESVersionError, match=r"not a known LEDES specification"
    ):
        get_parser(spec="a goose")

    with pytest.raises(UnsupportedLEDESVersionError, match=r"has not been written yet"):
        get_parser(spec="1998BI")


def test_get_parser_with_supported_spec():
    for spec in SUPPORTED_SPECS:
        try:
            parser = get_parser(spec=spec)
            assert parser is not None
        except Exception:
            pytest.fail(
                f"get_parser should have returned a parser for spec '{spec}' but raised an error instead."
            )
