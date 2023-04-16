import csv

from ledes_parser import parse_ledes_file


def test_parse_ledes_file_with_file_path_should_succeed():
    with open('tests/sample_data.txt', 'r') as f:
        reader = csv.reader(f, delimiter="|")
        invoices = parse_ledes_file(reader, "1998")

    assert len(invoices) > 0