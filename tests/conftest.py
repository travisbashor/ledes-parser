import os
import random
import string
from decimal import Decimal
from typing import List, Optional, Protocol, TypedDict, Union

import pytest
from faker import Faker
from faker.providers import BaseProvider
from lark import Lark


class LineItem1998B(TypedDict, total=False):
    invoice_date: str
    invoice_number: str
    client_id: str
    law_firm_matter_id: str
    invoice_total: str
    billing_start_date: str
    billing_end_date: str
    invoice_description: str
    line_item_number: str
    exp_fee_inv_adj_type: str
    line_item_number_of_units: str
    line_item_adjustment_amount: str
    line_item_total: str
    line_item_date: str
    line_item_task_code: str
    line_item_expense_code: str
    line_item_activity_code: str
    timekeeper_id: str
    line_item_description: str
    law_firm_id: str
    line_item_unit_cost: str
    timekeeper_name: str
    timekeeper_classification: str
    client_matter_id: str


HEADERS = (
    "INVOICE_DATE",
    "INVOICE_NUMBER",
    "CLIENT_ID",
    "LAW_FIRM_MATTER_ID",
    "INVOICE_TOTAL",
    "BILLING_START_DATE",
    "BILLING_END_DATE",
    "INVOICE_DESCRIPTION",
    "LINE_ITEM_NUMBER",
    "EXP/FEE/INV_ADJ_TYPE",
    "LINE_ITEM_NUMBER_OF_UNITS",
    "LINE_ITEM_ADJUSTMENT_AMOUNT",
    "LINE_ITEM_TOTAL",
    "LINE_ITEM_DATE",
    "LINE_ITEM_TASK_CODE",
    "LINE_ITEM_EXPENSE_CODE",
    "LINE_ITEM_ACTIVITY_CODE",
    "TIMEKEEPER_ID",
    "LINE_ITEM_DESCRIPTION",
    "LAW_FIRM_ID",
    "LINE_ITEM_UNIT_COST",
    "TIMEKEEPER_NAME",
    "TIMEKEEPER_CLASSIFICATION",
    "CLIENT_MATTER_ID",
)


def to_dict(line_item_text: str) -> dict:
    properties = (h.replace("/", "_").lower() for h in HEADERS)
    return {k: v for k, v in zip(properties, line_item_text.split("|"))}


class LineItemBuilder1998B:
    def __init__(self):
        self.field_values = dict()

    def empty_line_item(
        self, values: Optional[LineItem1998B] = {}
    ) -> "LineItemBuilder1998B":
        empty_row = "|".join(["" for _ in HEADERS])
        empty_line_item_data = to_dict(empty_row)
        self.field_values.update(empty_line_item_data)
        self.field_values.update(values)
        return self

    def fee(self, values: Optional[LineItem1998B] = {}) -> "LineItemBuilder1998B":
        sample_fee = "19990225|96542|00711|0528|1684.45|19990101|19990131|For services rendered|1|F|2.00|-70|630|19990115|L510||A102|22547|Research Attorney's fees, Set off claim|24-6437381|350|Arnsley, Robert|PARTNR|423-987"
        fee_data = to_dict(sample_fee)
        self.field_values.update(fee_data)
        self.field_values.update(values)
        return self

    def expense(self, values: Optional[LineItem1998B] = {}) -> "LineItemBuilder1998B":
        sample_expense = "19990225|96542|00711|0528|1684.45|19990101|19990131|For services rendered|4|E|1|0|24.95|19990117||E111|||Meals|24-6437381|24.95|||423-987"
        expense_data = to_dict(sample_expense)
        self.field_values.update(expense_data)
        self.field_values.update(values)
        return self

    def invoice_level_adjustment_to_fees(
        self, values: Optional[LineItem1998B] = {}
    ) -> "LineItemBuilder1998B":
        sample_fee_adjustment = "19990225|96543|00711|1326|1250|19990101|19990131|Monthly Retainer|6|IF|1|1250.|1250|19990131|||||Monthly Retainer Fee|24-6437381||||425-936"
        fee_adjustment_data = to_dict(sample_fee_adjustment)
        self.field_values.update(fee_adjustment_data)
        self.field_values.update(values)
        return self

    def invoice_level_adjustment_to_expenses(
        self, values: Optional[LineItem1998B] = {}
    ) -> "LineItemBuilder1998B":
        sample_expense_adjustment = "19990225|96543|00711|1326|1250|19990101|19990131|Monthly Retainer|6|IE|1|1250.|1250|19990131|||||Monthly Retainer Fee|24-6437381||||425-936"
        expense_adjustment_data = to_dict(sample_expense_adjustment)
        self.field_values.update(expense_adjustment_data)
        self.field_values.update(values)
        return self

    def build(self) -> str:
        """
        Returns the raw text of the line item and clears any accumulated values so it can be used again.
        """
        line_item_raw_text = "|".join(self.field_values.values())
        self.field_values.clear()
        return line_item_raw_text


class LEDES1998BBuilder:
    def __init__(self):
        LEDES_SPEC = "LEDES1998B"
        HEADERS = (
            "INVOICE_DATE",
            "INVOICE_NUMBER",
            "CLIENT_ID",
            "LAW_FIRM_MATTER_ID",
            "INVOICE_TOTAL",
            "BILLING_START_DATE",
            "BILLING_END_DATE",
            "INVOICE_DESCRIPTION",
            "LINE_ITEM_NUMBER",
            "EXP/FEE/INV_ADJ_TYPE",
            "LINE_ITEM_NUMBER_OF_UNITS",
            "LINE_ITEM_ADJUSTMENT_AMOUNT",
            "LINE_ITEM_TOTAL",
            "LINE_ITEM_DATE",
            "LINE_ITEM_TASK_CODE",
            "LINE_ITEM_EXPENSE_CODE",
            "LINE_ITEM_ACTIVITY_CODE",
            "TIMEKEEPER_ID",
            "LINE_ITEM_DESCRIPTION",
            "LAW_FIRM_ID",
            "LINE_ITEM_UNIT_COST",
            "TIMEKEEPER_NAME",
            "TIMEKEEPER_CLASSIFICATION",
            "CLIENT_MATTER_ID",
        )
        HEADER_ROW = "|".join(HEADERS)
        self.lines: List[str] = list([LEDES_SPEC, HEADER_ROW])

    def add_fee(self, line_item_total: Decimal) -> "LEDES1998BBuilder":
        return self.add_line_item(
            exp_fee_inv_adj_type="F", line_item_total=line_item_total or Decimal("0.00")
        )

    def add_line_item(self, **kwargs) -> "LEDES1998BBuilder":
        # This is a line item from the sample file for 98B from the LEDES website. Used as a base for testing.
        sample_line = "19990225|96542|00711|0528|1684.45|19990101|19990131|For services rendered|1|F|2.00|-70|630|19990115|L510||A102|22547|Research Attorney's fees, Set off claim|24-6437381|350|Arnsley, Robert|PARTNR|423-987"
        sample_values = sample_line.split("|")
        line = [
            kwargs.get("invoice_date", sample_values[0]),
            kwargs.get("invoice_number", sample_values[1]),
            kwargs.get("client_id", sample_values[2]),
            kwargs.get("law_firm_matter_id", sample_values[3]),
            kwargs.get("invoice_total", sample_values[4]),
            kwargs.get("billing_start_date", sample_values[5]),
            kwargs.get("billing_end_date", sample_values[6]),
            kwargs.get("invoice_description", sample_values[7]),
            kwargs.get("line_item_number", sample_values[8]),
            kwargs.get("exp_fee_inv_adj_type", sample_values[9]),
            kwargs.get("line_item_number_of_units", sample_values[10]),
            kwargs.get("line_item_adjustment_amount", sample_values[11]),
            kwargs.get("line_item_total", sample_values[12]),
            kwargs.get("line_item_date", sample_values[13]),
            kwargs.get("line_item_task_code", sample_values[14]),
            kwargs.get("line_item_expense_code", sample_values[15]),
            kwargs.get("line_item_activity_code", sample_values[16]),
            kwargs.get("timekeeper_id", sample_values[17]),
            kwargs.get("line_item_description", sample_values[18]),
            kwargs.get("law_firm_id", sample_values[19]),
            kwargs.get("line_item_unit_cost", sample_values[20]),
            kwargs.get("timekeeper_name", sample_values[21]),
            kwargs.get("timekeeper_classification", sample_values[22]),
            kwargs.get("client_matter_id", sample_values[23]),
        ]
        self.lines.append("|".join(line))
        return self

    def build(self) -> str:
        return "\n".join((line + "[]") for line in self.lines)


def fake_alphanumeric_id(length: int = 10) -> str:
    characters = string.ascii_letters + string.digits + "-"
    return "".join(random.choice(characters) for _ in range(length))


class InvoiceDataFaker(Protocol):
    def invoice_number(self, length: int = 10) -> str: ...

    def client_id(self, length: int = 10) -> str: ...

    def client_matter_id(self, length: int = 10) -> str: ...

    def law_firm_matter_id(self, length: int = 10) -> str: ...


class AlphanumericIDProvider(
    BaseProvider,
):
    def invoice_number(self, length: Optional[int] = None) -> str:
        return fake_alphanumeric_id(length or self.random_int(1, 20))

    def client_id(self, length: Optional[int] = None) -> str:
        return fake_alphanumeric_id(length or self.random_int(1, 20))

    def client_matter_id(self, length: Optional[int] = None) -> str:
        return fake_alphanumeric_id(length or self.random_int(1, 20))

    def law_firm_matter_id(self, length: Optional[int] = None) -> str:
        return fake_alphanumeric_id(length or self.random_int(1, 20))


@pytest.fixture(scope="session", autouse=True)
def invoice_faker() -> Union[Faker, InvoiceDataFaker]:
    # Create a Faker instance and add custom providers
    fake = Faker()
    fake.add_provider(AlphanumericIDProvider)
    return fake


# The parser may be session-scoped because parse() is idempotent.
@pytest.fixture(scope="session")
def line_item_parser():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    grammar_path = os.path.join(
        current_directory,
        "..",
        "ledes_parser",
        "grammars",
        "LEDES98B",
        "line_item.lark",
    )
    return Lark.open(grammar_path)


@pytest.fixture(scope="function", autouse=True)
def ledes_builder() -> LEDES1998BBuilder:
    return LEDES1998BBuilder()


@pytest.fixture(scope="function", autouse=True)
def line_item_builder() -> LineItemBuilder1998B:
    return LineItemBuilder1998B()
