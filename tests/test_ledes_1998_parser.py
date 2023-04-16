
import csv
from datetime import date
from ledes_parser.ledes_1998_parser import Ledes1998Parser


def test_ledes1998_parser():
    parser = Ledes1998Parser()
    with open('tests/sample_data.txt', 'r') as f:
        reader = csv.reader(f, delimiter="|")
        invoices = parser.parse(reader)

    assert len(invoices) > 0


def test_ledes1998_parser_should_parse_invoice_date():
    parser = Ledes1998Parser()
    with open('tests/sample_data.txt', 'r') as f:
        reader = csv.reader(f, delimiter="|")
        invoices = parser.parse(reader)

    first_invoice = invoices[0]
    invoice_date = first_invoice['invoice_date']
    assert isinstance(first_invoice['invoice_date'], date)
    assert invoice_date.year == 1999
    assert invoice_date.month == 2
    assert invoice_date.day == 25
