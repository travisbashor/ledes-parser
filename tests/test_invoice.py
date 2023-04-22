import random
from ledes_parser.typings.invoice_types import Invoice, LineItem


def test_invoice_wrong_line_item_total_should_be_invalid() -> None:
    # Create an invoice whose total isn't the sum of the line item totals.
    invoice = Invoice()
    invoice.invoice_total = 5  # bucks, maybe
    invoice.line_items = list()

    assert not invoice.is_valid(
    ), f"The invoice should be considered invalid, as the line item totals don't add up to the invoice total."


def test_invoice_exact_line_item_total_should_be_valid() -> None:
    invoice = Invoice()
    # Add 5 random line items.
    for _ in range(5):
        line_item = LineItem()
        line_item.line_item_total = round(
            (random.randrange(1, 100000)) / 100.00, 2)
        invoice.add_line_item(line_item)

    invoice.invoice_total = sum(
        (li.line_item_total for li in invoice.line_items))
    assert invoice.is_valid()


def test_invoice_line_item_total_within_tolerance_below_should_be_valid() -> None:
    invoice = Invoice()
    # Add 5 random line items.
    for _ in range(5):
        line_item = LineItem()
        line_item.line_item_total = round(
            (random.randrange(1, 100000)) / 100.00, 2)
        invoice.add_line_item(line_item)

    invoice.invoice_total = 0.991 * sum(
        (li.line_item_total for li in invoice.line_items))
    assert invoice.is_valid()


def test_invoice_line_item_total_within_tolerance_above_should_be_valid() -> None:
    invoice = Invoice()
    # Add 5 random line items.
    for _ in range(5):
        line_item = LineItem()
        line_item.line_item_total = round(
            (random.randrange(1, 100000)) / 100.00, 2)
        invoice.add_line_item(line_item)

    invoice.invoice_total = 1.009 * sum(
        (li.line_item_total for li in invoice.line_items))
    assert invoice.is_valid()

def test_invoice_line_item_total_outside_tolerance_above_should_be_invalid() -> None:
    invoice = Invoice()
    # Add 5 random line items.
    for _ in range(5):
        line_item = LineItem()
        line_item.line_item_total = round(
            (random.randrange(1, 100000)) / 100.00, 2)
        invoice.add_line_item(line_item)

    invoice.invoice_total = 1.011 * sum(
        (li.line_item_total for li in invoice.line_items))
    assert not invoice.is_valid()

def test_invoice_line_item_total_outside_tolerance_below_should_be_invalid() -> None:
    invoice = Invoice()
    # Add 5 random line items.
    for _ in range(5):
        line_item = LineItem()
        line_item.line_item_total = round(
            (random.randrange(1, 100000)) / 100.00, 2)
        invoice.add_line_item(line_item)

    invoice.invoice_total = 0.989 * sum(
        (li.line_item_total for li in invoice.line_items))
    assert not invoice.is_valid()
