from typing import List, TextIO

from base_ledes_parser import BaseLedesParser

from .typings.invoice_types import Invoice


class Ledes1998BIParser(BaseLedesParser):
    def parse(self, reader: TextIO) -> List[Invoice]:
        invoices = []
        for row in reader:
            pass
            # Parse fields according to the 1998BI format
            # ...
        return invoices
