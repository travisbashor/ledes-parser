from datetime import datetime
from typing import List, TextIO

from ledes_parser.base_ledes_parser import BaseLedesParser

from .typings.invoice_types import Invoice


class Ledes1998Parser(BaseLedesParser):
    def parse(self, reader: TextIO) -> List[Invoice]:
        invoices = []

        # Skip the format spec and header lines.
        print(next(reader))
        print(next(reader))
        for row in reader:
            # Parse fields according to the 1998 format.
            if not row:
                continue

            current_invoice = Invoice()
            date_str = row[0]
            current_invoice['invoice_date'] = datetime.strptime(date_str, "%Y%m%d")

            invoices.append(current_invoice)

        return invoices
