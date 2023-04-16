from datetime import datetime
import logging
from typing import Iterable, List

from ledes_parser.base_ledes_parser import BaseLedesParser

from .typings.invoice_types import Invoice, LineItem
from csv import reader

class Ledes1998BParser(BaseLedesParser):
    def parse(self, csv_data: Iterable[str]) -> List[Invoice]:
        invoices = []
        csv_reader = reader(csv_data, delimiter="|")

        # First line contains the ledes format.
        next(csv_reader)

        # Second line contains the column headers.
        next(csv_reader)

        row_number = 2
        for row in csv_reader:
            row_number += 1
            # Parse invoice according to https://ledes.org/ledes-98b-format/#
            if not row:
                continue

            current_invoice = Invoice()

            current_invoice.invoice_number = row[1]
            logging.debug(f"Parsing invoice number '{row[1]}' on row {row_number}.")

            current_invoice.invoice_date = datetime.strptime(row[0], "%Y%m%d")
            current_invoice.client_id = row[2]
            current_invoice.law_firm_matter_id = row[3]
            current_invoice.invoice_total = row[4]
            current_invoice.billing_start_date = datetime.strptime(row[5], "%Y%m%d")
            current_invoice.billing_end_date = datetime.strptime(row[6], "%Y%m%d")
            current_invoice.invoice_description = row[7]
            current_invoice.client_matter_id = row[23]

            current_line_item = LineItem()
            current_line_item.line_item_number = row[8]
            current_line_item.exp_fee_inv_adj_type = row[9]
            current_line_item.number_of_units = row[10]
            current_line_item.adjustment_amount = 0 if row[11] == '' else float(row[11])
            current_line_item.line_item_total = float(row[12])
            current_line_item.line_item_date = datetime.strptime(row[13], "%Y%m%d")
            current_line_item.task_code = row[14]
            current_line_item.expense_code = row[15]
            current_line_item.activity_code = row[16]
            current_line_item.timekeeper_id = row[17]
            current_line_item.description = row[18]
            current_line_item.law_firm_id = row[19]
            current_line_item.unit_cost = 0 if row[20] == '' else float(row[20])
            current_line_item.timekeeper_name = row[21]
            current_line_item.timekeeper_classification = row[22]

            current_invoice.line_items.append(current_line_item)

            invoices.append(current_invoice)

        return invoices
