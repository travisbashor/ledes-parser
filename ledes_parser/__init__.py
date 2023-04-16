from typing import List, TextIO

from ledes_parser.ledes_1998_parser import Ledes1998Parser
from ledes_parser.ledes_1998B_parser import Ledes1998BParser
from ledes_parser.ledes_1998BI_parser import Ledes1998BIParser

from .typings.invoice_types import Invoice


def parse_ledes_file(file: TextIO, ledes_format: str) -> List[Invoice]:
    """
    Parses a LEDES file based on the provided format and returns a list of Invoice objects.

    :param file: A file-like object (TextIO) containing the LEDES data to parse.
    :param ledes_format: A string specifying the LEDES format of the input data.
                         Supported formats are "1998", "1998B", and "1998BI".
    :raises ValueError: If an unsupported format is provided.
    :return: A list of Invoice objects representing the parsed invoice data.

    Usage:
    ```
    with open('path/to/your/ledes_file.txt', 'r') as f:
        reader = csv.reader(f, delimiter="|")
        invoices = parse_ledes_file(reader, '1998')
    """
    parser = None
    if ledes_format == '1998':
        parser = Ledes1998Parser()
    elif ledes_format == '1998B':
        parser = Ledes1998BParser()
    elif ledes_format == '1998BI':
        parser = Ledes1998BIParser()
    else:
        raise ValueError(f'Unsupported format: {ledes_format}')

    return parser.parse(file)
