from typing import List, TypedDict

class LineItem(TypedDict):
    line_number: int
    timekeeper_id: str
    hours: float
    rate: float
    task_code: str
    activity_code: str
    line_total: float

class Invoice(TypedDict):
    invoice_number: str
    client_id: str
    invoice_date: str
    invoice_total: float
    invoice_lines: List[LineItem]
