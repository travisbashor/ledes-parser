from typing import List, TextIO

from ledes_parser.base_ledes_parser import BaseLedesParser

from .typings.invoice_types import Invoice


class Ledes1998BParser(BaseLedesParser):
    def parse(self, reader: TextIO) -> List[Invoice]:
        invoices = []
        for row in reader:
            pass
            # Parse fields according to the 1998B format
            # ...
        return invoices
