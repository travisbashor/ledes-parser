from typing import List

# from lark import Lark

LINE_ENDING_TOKEN_NAME = "_LINE_ENDING"
SEPARATOR_TOKEN_NAME = "_SEP"


def rule(rule_name: str, rule_body: str) -> str:
    return rule_name + ": " + rule_body


def line(text: str) -> str:
    return text + " _LINE_ENDING"


def separated(tokens: List[str], separator_token_name: str = "_SEP") -> str:
    return f" {separator_token_name} ".join(tokens)


def header_token(token_name: str) -> str:
    return "header_" + token_name  # header_invoice_date, header_invoice_number, etc...


def literal(some_string: str) -> str:
    return f'"{some_string}"'


def any_of(tokens: List[str]) -> str:
    return "(" + " | ".join(tokens) + ")"


# Define a function to generate the grammar with given tokens.
def generate_grammar(spec: str, data_element_tokens: List[str]):
    start_rule = rule("?start", "specification headers line_item+")

    specification_rule = rule(
        "specification", line(literal(spec))
    )  # "LEDES1998B[]", for example

    headers_rule = rule(
        "headers", line(separated([header_token(t) for t in data_element_tokens]))
    )

    # line_item: fee | expense | invoice_level_fee_adjustment | invoice_level_expense_adjustment
    line_item_types = [
        "fee",
        "expense",
        "invoice_level_fee_adjustment",
        "invoice_level_expense_adjustment",
    ]
    line_item_rule = rule("line_item", line(any_of(line_item_types)))
    rules = [start_rule, specification_rule, headers_rule, line_item_rule]
    rule_definitions = "\n\n".join(rules)
    non_terminal_symbols = "\n".join(["// Non-terminal symbols"])
    terminal_symbols = "\n".join(
        [
            "// Terminal symbols",
            rule("_LINE_ENDING", literal("[]")),
            rule("_SEP", literal("|")),
        ]
    )
    directives = """
%import common.WS
%ignore WS
    """

    grammar = "\n\n".join(
        [rule_definitions, non_terminal_symbols, terminal_symbols, directives]
    )

    return grammar


if __name__ == "__main__":
    # List of tokens
    tokens = ["invoice_date", "invoice_number"]

    # Generate the grammar
    grammar = generate_grammar("1998B", tokens)
    print(f"Generated Grammar:\n{grammar}")

    # # Create the parser
    # parser = Lark(grammar, parser="lalr")

    # # Example usage
    # data = "A, B, C"

    # try:
    #     result = parser.parse(data)
    #     print("Parsing successful!")
    #     print(result.pretty())
    # except Exception as e:
    #     print(f"Error: {e}")
