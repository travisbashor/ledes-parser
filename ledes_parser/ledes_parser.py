import pkg_resources
from lark import Lark


# TODO: Constrain this to just the known specs.
def get_parser(spec: str) -> Lark:
    """
    @returns A parser that can read ledes text in the given ledes spec (e.g., 98B, 98BI, etc...).
    """
    supported_specs = ["98B"]
    if spec not in supported_specs:
        raise ValueError(
            f"Unrecognized ledes spec: '{spec}'. Supported specs are: {supported_specs}"
        )
    # By convention, the grammar for a spec is in: grammars/spec_<the-spec>/main_grammar.lark
    main_grammar_file = f"grammars/spec_{spec.upper()}/main_grammar.lark"
    path_to_grammar = pkg_resources.resource_filename(__name__, main_grammar_file)
    import_paths = pkg_resources.resource_filename(
        __name__, f"grammars/spec_{spec.upper()}"
    )
    return Lark.open(
        path_to_grammar, start="start", parser="lalr", import_paths=[import_paths]
    )
