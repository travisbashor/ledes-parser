#!/usr/bin/env python3

from typing import List

LINE_ENDING_TOKEN_NAME = "_LINE_ENDING"
SEPARATOR_TOKEN_NAME = "_SEP"


def comment(comment: str) -> str:
    return "// " + comment


def rule(rule_name: str, rule_body: str) -> str:
    return rule_name + ": " + rule_body


def line(text: str) -> str:
    return text + " _LINE_ENDING"


def separated(tokens: List[str], separator_token_name: str = "_SEP") -> str:
    return f" {separator_token_name} ".join(tokens)


def header(token_name: str) -> str:
    return "header_" + token_name


def literal(some_string: str) -> str:
    return f'"{some_string}"'


def any_of(tokens: List[str]) -> str:
    return "(" + " | ".join(tokens) + ")"


def create_headers() -> str: ...


def create_terminals() -> str: ...


def create_directives() -> str:
    directives = ("%import common.WS", "%ignore WS")
    return "\n".join(("// Directives", *directives))


# Define a function to create the grammar with given tokens.
def create_grammar(spec: str, tokens: List[str]):
    lines: List[str] = list()
    lines.append(comment("LEDES1998B[]"))
    lines.append(comment("INVOICE_DATE|INVOICE_NUMBER|...|CLIENT_MATTER_ID[]"))
    lines.append(comment("20240209|ABC-123|...|CM-500[]"))

    # Start rule; the entrypoint
    lines.append(rule("?start", "specification headers line_item+"))
    lines.append("")

    # "LEDES1998B[]", for example
    ledes_version_rule = rule("specification", line(literal(spec)))

    # headers: header_invoice_date _SEP header_invoice_number _SEP header_...
    headers_rule = rule("headers", line(separated([header(t) for t in tokens])))
    header_tokens = [(header(t).upper(), literal(t.upper())) for t in tokens]

    # line_item: fee | expense | invoice_level_fee_adjustment | invoice_level_expense_adjustment
    line_item_types = (
        "fee",
        "expense",
        "invoice_level_fee_adjustment",
        "invoice_level_expense_adjustment",
    )
    line_item_rule = rule("line_item", line(any_of(line_item_types)))

    rules = [ledes_version_rule, headers_rule, line_item_rule]
    rule_definitions = "\n\n".join(rules)

    non_terminal_symbols = "\n".join(["// Non-terminal symbols"])
    terminal_symbols = "\n".join(
        [
            "// Terminal symbols",
            rule("LEDES_SPEC", literal(spec)),
            rule("_SEP", literal("|")),
            rule("_LINE_ENDING", literal("[]")),
            *[rule(token_name, token_defn) for token_name, token_defn in header_tokens],
        ]
    )

    directives = create_directives()

    grammar = "\n\n".join(
        [rule_definitions, non_terminal_symbols, terminal_symbols, directives]
    )

    return grammar


if __name__ == "__main__":
    # Example: List of tokens
    tokens = ["invoice_date", "invoice_number"]

    # Generate the grammar
    grammar = create_grammar("LEDES1998B", tokens)
    print(grammar)

    # # Create the parser
    # from lark import Lark
    # parser = Lark(grammar, parser="lalr")

    # try:
    #     result = parser.parse(data)
    #     print("Parsing successful!")
    #     print(result.pretty())
    # except Exception as e:
    #     print(f"Error: {e}")
