from typing import List, TextIO
from base_ledes_parser import BaseLedesParser
from .typings.invoice_types import Invoice

class Ledes1998Parser(BaseLedesParser):
    def parse(self, reader: TextIO) -> List[Invoice]:
        invoices = []
        for row in reader:
            # Parse fields according to the 1998 format.
            if not row:
                continue

            record_type = row[0]



            if record_type == 'INVOICE':
                invoice = {
                    'invoice_number': row[1],
                    'client_id': row[2],
                    'invoice_date': row[3],
                    'invoice_total': row[4],
                    'bill_to': row[5],
                    'invoice_description': row[6],
                    'line_item_count': row[7],
                    'invoice_lines': []
                }
                invoices.append(invoice)
            elif record_type == 'LINE':
                invoice_line = {
                    'line_number': row[1],
                    'expense_date': row[2],
                    'timekeeper_id': row[3],
                    'timekeeper_name': row[4],
                    'hours': row[5],
                    'rate': row[6],
                    'task_code': row[7],
                    'activity_code': row[8],
                    'description': row[9],
                    'line_total': row[10]
                }
                invoices[-1]['invoice_lines'].append(invoice_line)

        return invoices
