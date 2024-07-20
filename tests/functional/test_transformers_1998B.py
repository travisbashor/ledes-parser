from datetime import datetime
from decimal import Decimal
from typing import Any

import pytest
from lark import Lark

from ledes_parser import get_parser
from ledes_parser.transformers.transformer_1998B import LineItemTransformer
from tests.conftest import LineItemBuilder1998B


@pytest.fixture(scope="module", autouse=True)
def line_item_transformer() -> LineItemTransformer:
    return LineItemTransformer()


def test_transform_valid_line_item_succeeds(
    line_item_parser: Lark,
    line_item_transformer: LineItemTransformer,
    line_item_builder: LineItemBuilder1998B,
):
    # Produce the abstract syntax tree for this line item.
    line_item = line_item_builder.fee().build()
    fee_ast = line_item_parser.parse(line_item)

    # Attempt to map it into a python dict.
    fee = line_item_transformer.transform(fee_ast)
    assert fee is not None
    assert isinstance(fee, dict)


@pytest.mark.parametrize(
    "field_name,token,expected_value",
    [
        ("invoice_date", "20130423", datetime(2013, 4, 23)),
        ("invoice_number", "8675309", "8675309"),
        ("client_id", "ABC-900", "ABC-900"),
        ("law_firm_matter_id", "DEF000", "DEF000"),
        ("invoice_total", "5.00", Decimal("5.00")),
        ("billing_start_date", "20240101", datetime(2024, 1, 1)),
        ("billing_end_date", "20240131", datetime(2024, 1, 31)),
        (
            "invoice_description",
            "Some description. Might have spaces; might have punctuation!",
            "Some description. Might have spaces; might have punctuation!",
        ),
        ("line_item_number", "1", "1"),
        ("line_item_number_of_units", "50.00", Decimal("50.00")),
        ("line_item_adjustment_amount", "+1.2", Decimal("+1.2")),
        ("line_item_adjustment_amount", "-1.2", Decimal("-1.2")),
        ("line_item_total", "55.00", Decimal("55.00")),
        ("line_item_date", "20190504", datetime(2019, 5, 4)),
        ("line_item_task_code", "P220", "P220"),
        ("line_item_expense_code", "E101", "E101"),
        ("line_item_activity_code", "A101", "A101"),
        ("timekeeper_id", "AP555", "AP555"),
        ("line_item_description", "For services rendered.", "For services rendered."),
        ("law_firm_id", "LF-001", "LF-001"),
        ("line_item_unit_cost", "99.00", Decimal("99.00")),
        ("timekeeper_name", "Haroldson, Harold Esq.", "Haroldson, Harold Esq."),
        ("timekeeper_classification", "PARTNR", "PARTNR"),
        ("client_matter_id", "M-01", "M-01"),
    ],
)
def test_transform_maps_each_property(
    line_item_builder: LineItemBuilder1998B,
    line_item_parser: Lark,
    line_item_transformer: LineItemTransformer,
    field_name: str,
    token: str,
    expected_value: Any,
):
    line_item_values = dict.fromkeys((field_name,), token)
    line_item = line_item_builder.fee(line_item_values).build()
    fee_ast = line_item_parser.parse(line_item)

    # Attempt to map it into a python dict.
    fee = line_item_transformer.transform(fee_ast)
    assert fee[field_name] == expected_value


def test_transform_maps_valid_ledes_text():
    parser_with_transformer = get_parser(spec="1998B", ast_only=False)
    valid_ledes_text = """
LEDES1998B[]
INVOICE_DATE|INVOICE_NUMBER|CLIENT_ID|LAW_FIRM_MATTER_ID|INVOICE_TOTAL|BILLING_START_DATE|BILLING_END_DATE|INVOICE_DESCRIPTION|LINE_ITEM_NUMBER|EXP/FEE/INV_ADJ_TYPE|LINE_ITEM_NUMBER_OF_UNITS|LINE_ITEM_ADJUSTMENT_AMOUNT|LINE_ITEM_TOTAL|LINE_ITEM_DATE|LINE_ITEM_TASK_CODE|LINE_ITEM_EXPENSE_CODE|LINE_ITEM_ACTIVITY_CODE|TIMEKEEPER_ID|LINE_ITEM_DESCRIPTION|LAW_FIRM_ID|LINE_ITEM_UNIT_COST|TIMEKEEPER_NAME|TIMEKEEPER_CLASSIFICATION|CLIENT_MATTER_ID[]
19990225|96542|00711|0528|1684.45|19990101|19990131|For services rendered|1|F|2.00|-70|630|19990115|L510||A102|22547|Research Attorney's fees, Set off claim|24-6437381|350|Arnsley, Robert|PARTNR|423-987[]
19990225|96542|00711|0528|1684.45|19990101|19990131|For services rendered|2|F|2.00|0|700|19990115|L510||A102|22547|Research attorney's fees, Trial pleading|24-6437381|350|Arnsley, Robert|PARTNR|423-987[]
19990225|96542|00711|0528|1684.45|19990101|19990131|For services rendered|3|F|0.200|0|40|19990116|L510||A107|45875|Telephone conference with John Doe|24-6437381|200|Beaster, John|ASSOC|423-987[]
19990225|96542|00711|0528|1684.45|19990101|19990131|For services rendered|4|E|1|0|24.95|19990117||E111|||Meals|24-6437381|24.95|||423-987[]
19990225|96542|00711|0528|1684.45|19990101|19990131|For services rendered|5|E|1|0|289.5|19990117||E110|||Out-of_town travel|24-6437381|289.5|||423-987[]
19990225|96543|00711|1326|1250|19990101|19990131|Monthly Retainer|6|IF|1|1250.|1250|19990131|||||Monthly Retainer Fee|24-6437381||||425-936[]
19990225|96543|500|500.900|1250|19990101|19990131|Monthly Retainer|6|IF|1|1250.|1250|19990131|||||Monthly Retainer Fee|24-6437381||||425-936[]
"""
    result = parser_with_transformer.parse(valid_ledes_text)
    assert result is not None
    assert isinstance(result, dict)
