import csv
from typing import List, TextIO
from ledes_1998_parser import Ledes1998Parser
from ledes_1998B_parser import Ledes1998BParser
from ledes_1998BI_parser import Ledes1998BIParser
from .typings.invoice_types import Invoice

def parse_ledes_file(file_path: TextIO, ledes_format: str) -> List[Invoice]:
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')

        parser = None
        if format == '1998':
            parser = Ledes1998Parser()
        elif format == '1998B':
            parser = Ledes1998BParser()
        elif format == '1998BI':
            parser = Ledes1998BIParser()
        else:
            raise ValueError(f'Unsupported format: {format}')

        return parser.parse(reader)
