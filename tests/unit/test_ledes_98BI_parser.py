import os

import pytest
from lark import Lark, UnexpectedInput


@pytest.fixture(scope="module")
def parser():
    base_path = os.path.dirname(os.path.abspath(__file__))
    path_to_grammar = os.path.join(
        base_path, "../../ledes_parser/grammars/LEDES98BI/line_item.lark"
    )
    import_paths = os.path.join(base_path, "../../ledes_parser/grammars/")
    return Lark.open(
        path_to_grammar,
        start="start",
        parser="lalr",
        import_paths=[import_paths],
    )


def test_basic_line_item_parsing(parser):
    sample_line_items = [
        "20080225|96542|711|528|1869.97|20080101|20080131|For services rendered|1|F|2|-70|717.63|20080115|L510||A102|22547|Research Attorney's fees Set off claim|24-6437381|350|Arnsley Robert|PARTNR|423-987|77654|76-1235|Merten Merger|182.52|1781.16|GBP|Arnsley|Robert|O|Law Offices of John Smith|One Fleet Street||London||EC2A 2EG|GBR|Stanley's Widgets|One Times Square||New York|NY|10036|USA|0.061245|87.63|VAT|182.52|GBP",
        "20080225|96542|711|528|1869.97|20080101|20080131|For services rendered|2|F|2|0|792.6|20080115|L510||A102|22547|Research attorney's fees Trial pleading|24-6437381|350|Arnsley Robert|PARTNR|423-987|77654|76-1235|Merten Merger|182.52|1781.16|GBP|Arnsley|Robert|O|Law Offices of John Smith|One Fleet Street||London||EC2A 2EG|GBR|Stanley's Widgets|One Times Square||New York|NY|10036|USA|0.061245|92.6|VAT|182.52|GBP",
        "20080225|96542|711|528|1869.97|20080101|20080131|For services rendered|3|F|0.2|0|45.29|20080116|L510||A107|45875|Telephone conference with John Doe|24-6437381|200|Beaster John|ASSOC|423-987|77654|76-1235|Merten Merger|182.52|1781.16|GBP|Beaster|John|O|Law Offices of John Smith|One Fleet Street||London||EC2A 2EG|GBR|Stanley's Widgets|One Times Square||New York|NY|10036|USA|0.061245|5.29|VAT|182.52|GBP",
        "20080225|96542|711|528|1869.97|20080101|20080131|For services rendered|4|E|1|0|24.95|20080117||E111|||Meals|24-6437381|24.95|||423-987|77654|76-1235|Merten Merger|182.52|1781.16|GBP|||O|Law Offices of John Smith|One Fleet Street||London||EC2A 2EG|GBR|Stanley's Widgets|One Times Square||New York|NY|10036|USA|0|0|VAT|182.52|GBP",
        "20080225|96542|711|528|1869.97|20080101|20080131|For services rendered|5|E|1|0|289.5|20080117||E110|||Out-of_town travel|24-6437381|289.5|||423-987|77654|76-1235|Merten Merger|182.52|1781.16|GBP|||O|Law Offices of John Smith|One Fleet Street||London||EC2A 2EG|GBR|Stanley's Widgets|One Times Square||New York|NY|10036|USA|0|0|VAT|182.52|GBP",
        "20080225|96543|711|1326|1338.81|20080101|20080131|Monthly Retainer|6|IF|1|0|1338.81|20080131|||||Monthly Retainer Fee|24-6437381|1250|||425-936||76-1235|Somos Merger|88.81|1250|GBP|||O|Law Offices of John Smith|One Fleet Street||London||EC2A 2EG|GBR|Stanley's Widgets|One Times Square||New York|NY|10036|USA|0.061245|88.81|VAT|88.81|GBP",
    ]

    for line_item in sample_line_items:
        try:
            parsed = parser.parse(line_item)
            assert parsed is not None
            print("Parse tree:", parsed.pretty())
        except UnexpectedInput as e:
            pytest.fail(f"Parsing failed with an unexpected input: {e}")


def test_invalid_line_item(parser):
    # Test an invalid line item to ensure it raises an exception
    line_item_with_fields_missing = "19990225|96542|00711"  # Missing fields

    with pytest.raises(UnexpectedInput):
        parser.parse(line_item_with_fields_missing)
