import json
from typing import List, TextIO

from .typings.invoice_types import Invoice

field_to_property_map = {
  'INVOICE_DATE': 'invoice_date'
}

class DynamicLEDESParser:
    def __init__(self, format_file: str):
        with open(format_file, 'r') as f:
            self.format_data = json.load(f)
        self.field_codes = [field["code"] for field in self.format_data["fields"]]

    def parse(self, input_data: TextIO) -> List[Invoice]:
        invoices = []
        for line in input_data:
            line_parts = line.strip().split('\t')
            invoice_data = {}
            for idx, field_code in enumerate(self.field_codes):
                invoice_data[field_code] = line_parts[idx]
            invoices.append(Invoice(**invoice_data))
        return invoices

# Usage example
parser = DynamicLEDESParser('path/to/ledes_1998.json')

with open('path/to/ledes_file.txt', 'r') as file:
    invoices = parser.parse(file)

print(invoices)
