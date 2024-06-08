from lark import Lark

SAMPLE_LEDES: str = """
LEDES1998B[]
INVOICE_DATE|INVOICE_NUMBER|CLIENT_ID|LAW_FIRM_MATTER_ID|LINE_ITEM_NUMBER|EXP/FEE/INV_ADJ_TYPE|LINE_ITEM_DESCRIPTION|LINE_ITEM_AMOUNT|LINE_ITEM_TAX_RATE|LINE_ITEM_TAX_TYPE|LINE_ITEM_TASK_CODE|LINE_ITEM_EXPENSE_CODE|TIMEKEEPER_ID|TIMEKEEPER_LEVEL|LINE_ITEM_UNIT_COST|LINE_ITEM_QUANTITY|LINE_ITEM_ADJUSTMENT_AMOUNT|LINE_ITEM_TOTAL|LINE_ITEM_DATE|LAW_FIRM_ID|BILLING_START_DATE|BILLING_END_DATE|INVOICE_DESCRIPTION|BILLING_CONTACT|CLIENT_MATTER_ID|TIMEKEEPER_NAME|TIMEKEEPER_CLASSIFICATION|TIMEKEEPER_HOURLY_RATE[]
20240101|INV-001|CL-123|LM-456|1|F|Review of documents|500.00|0.00|||DOC|TK-001|Senior Partner|500.00|1|0.00|500.00|20240101|LF-789|20240101|20240131|January legal services|John Doe|CM-123|Jane Smith|Partner|550.00[]
20240102|INV-001|CL-123|LM-456|2|F|Preparation of legal brief|750.00|0.00|||BRIEF|TK-002|Associate|375.00|2|0.00|750.00|20240102|LF-789|20240101|20240131||John Doe|CM-123|John Doe|Associate|375.00[]
"""


def get_parser() -> Lark:
    """
    @returns A parser that can read ledes 98B text.
    """
    # Load the ledes 98B grammar and return a parser for it.
    with open("./grammars/ledes_98B_grammar.lark") as grammar_file:
        ledes_98B_grammar = grammar_file.read()

    return Lark(grammar=ledes_98B_grammar, start="start", parser="lalr")


def show_ledes_file_data() -> None:
    ledes_98B_parser = get_parser()
    parse_tree = ledes_98B_parser.parse(SAMPLE_LEDES)
    print(parse_tree.pretty())


if __name__ == "__main__":
    # Parse a ledes 98B file and show what was parsed out for each token.
    show_ledes_file_data()
