import unittest

from ledes_parser import get_parser
from tests.conftest import LEDES1998BBuilder


class TestLedes98BParser(unittest.TestCase):
    def setUp(self):
        self.parser = get_parser(spec="1998B", ast_only=True)
        self.ledes_builder = LEDES1998BBuilder()

    def test_parse_valid_data(self):
        data = """
LEDES1998B[]
INVOICE_DATE|INVOICE_NUMBER|CLIENT_ID|LAW_FIRM_MATTER_ID|INVOICE_TOTAL|BILLING_START_DATE|BILLING_END_DATE|INVOICE_DESCRIPTION|LINE_ITEM_NUMBER|EXP/FEE/INV_ADJ_TYPE|LINE_ITEM_NUMBER_OF_UNITS|LINE_ITEM_ADJUSTMENT_AMOUNT|LINE_ITEM_TOTAL|LINE_ITEM_DATE|LINE_ITEM_TASK_CODE|LINE_ITEM_EXPENSE_CODE|LINE_ITEM_ACTIVITY_CODE|TIMEKEEPER_ID|LINE_ITEM_DESCRIPTION|LAW_FIRM_ID|LINE_ITEM_UNIT_COST|TIMEKEEPER_NAME|TIMEKEEPER_CLASSIFICATION|CLIENT_MATTER_ID[]
19990225|96542|00711|0528|1684.45|19990101|19990131|For services rendered|1|F|2.00|-70|630|19990115|L510||A102|22547|Research Attorney's fees, Set off claim|24-6437381|350|Arnsley, Robert|PARTNR|423-987[]
19990225|96542|555|555.900|1684.45|19990101|19990131|For services rendered|1|F|2.00|-70|630|19990115|L510||A102|22547|Research Attorney's fees, Set off claim|24-6437381|350|Arnsley, Robert|PARTNR|423-987[]
19990225|96542|555|555.900|1053.|19990101|19990131|For services rendered|1|F|2.00|-70|630|19990115|L510||A102|22547|Research Attorney's fees, Set off claim|24-6437381|350|Arnsley, Robert|PARTNR|423-987[]
19990225|96542|555|555.900|1053.0|19990101|19990131|For services rendered|1|F|2.00|-70|630|19990115|L510||A102|22547|Research Attorney's fees, Set off claim|24-6437381|350|Arnsley, Robert|PARTNR|423-987[]
19990225|96542|555|555.900|1053.00|19990101|19990131|For services rendered|1|F|2.00|-70|630|19990115|L510||A102|22547|Research Attorney's fees, Set off claim|24-6437381|350|Arnsley, Robert|PARTNR|423-987[]
19990225|96542|555|555.900|1053.000|19990101|19990131|For services rendered|1|F|2.00|-70|630|19990115|L510||A102|22547|Research Attorney's fees, Set off claim|24-6437381|350|Arnsley, Robert|PARTNR|423-987[]
19990225|96542|555|555.900|1053.0000|19990101|19990131|For services rendered|1|F|2.00|-70|630|19990115|L510||A102|22547|Research Attorney's fees, Set off claim|24-6437381|350|Arnsley, Robert|PARTNR|423-987[]
"""
        result = self.parser.parse(data)
        self.assertIsNotNone(result)
        self.assertIn("LEDES1998B", result.pretty())

    def test_can_parse_valid_invoice_date(self):
        ledes_text = self.ledes_builder.add_line_item(invoice_date="20220101").build()

        result = self.parser.parse(ledes_text)
        self.assertIsNotNone(result)
        self.assertIn("20220101", result.pretty())

    def test_can_parse_wacky_non_separator_characters_in_description(self):
        nonsense = "And then The Lord Said: &;𓂀𝔾𝕠𝔹𐐝ꙨǰљᛗᎴᙔᗧ᚜𐎄𓆏𝓐ɆɮԱԲԳԴ𒀱𐌿𐑄𑂺𑄿𑍋ᜩᝰᠮᡶᢚᣣᤴᥑᦶᨛ᩠᪳᭗᮵᯼ᰢᱵ𐒶𐖶𐞻𑚳𑡦𑴈𑵑𒐅𓃒𓂺𓀏𓇽𓉲𓍯𓏮𓐅𓊲𓍄𓄞𓃠𓅃𓀗𓊞𓏲𓇅𓈋𓌔𓐭𓉂𓄯𓅦𓀉𓃴𓇎𓆸𓊵𓋛𓌥𓍑𓎳𓏒𓑟𓃠𓅎𓆡𓇶𓈈𓉦𓋒𓍀𓐮𓏫𓎅𓀕𓇼𓆆𓌤𓋇𓌬𓍬𓏔𓑆𓀛𓀔𓂿𓅂𓇷𓆾𓊮𓋩𓌿𓍌𓏆𓑀𓀁𓆕𓉅𓊉𓏻𓇰𓆲𓍍𓍇𓑋𓄆𓋖𓏘𓀆𓇍𓇐𓇷𓇑𓇳𓈚𓉨𓋾𓌻𓍗𓏁𓏀𓏣𓏪𓐮𓑕𓑤𓆟𓋶𓋥𓏱𓉗𓉝𓋴𓍍𓏰𓏪𓑖𓑙𓀃𓀆𓂟𓃬𓆉𓆮𓇥𓈜𓉃𓋜𓌶𓍄𓏠𓀈𓀜𓁌𓄠𓅀𓅟𓆿𓈊𓉟𓋫𓌺𓏦𓏬𓏿𓍉𓀙𓆃𓆂𓆊𓇽𓉕𓋐𓋲𓌯𓎝𓏎𓏰𓐶𓑡𓑭𓊂𓊹𓊷𓋼𓌃𓏆𓐳𓑕𓏥𓍀𓏿𓍏𓀍𓀜𓀟𓁌𓂁𓂡𓂹𓃫𓆡𓈋𓈛𓉘𓋾𓌼𓍀𓏘𓏹𓐿𓍛𓊛𓀃𓂻𓃫𓆠𓆱𓇽𓉌𓋉𓌶𓍐𓏮𓐑𓐩𓑦𓒀𓓀𓓉𓓘𓓲𓔂𓔌𓔍𓔫𓕇𓕟𓕨𓕫𓕭𓕳𓖀𓖇𓖙𓖝𓖯𓗃𓗈𓗏𓗕𓗘𓗢𓗤𓗬𓗰𓗾𓘀𓘂𓘅𓘆𓘎𓘐𓘙𓘞𓘠𓘫𓘰𓘴𓘺𓘽𓘾𓘿𓙀𓙁𓙂𓙃𓙄𓙆𓙊𓙋𓙌𓙍𓙏𓙐𓙑𓙒𓙕𓙖𓙗𓙘𓙙𓙚𓙛𓙜𓙝𓙞𓙟𓙠𓙡𓙢𓙣𓙤𓙥𓙦𓙧𓙨𓙩𓙪𓙫𓙬𓙭𓙮𓙯𓙰𓙱𓙲𓙳𓙴𓙵𓙶𓙷𓙸𓙹𓙺𓙻𓙼𓙽𓙾𓙿𓚀𓚁𓚂𓚃𓚄𓚅𓚆𓚇𓚈𓚉𓚊𓚋𓚌𓚍𓚎𓚏𓚐𓚑𓚒𓚓𓚔𓚕𓚖𓚗𓚘𓚙𓚚𓚛𓚜𓚝𓚞𓚟𓚠𓚡𓚢𓚣𓚤𓚥𓚦𓚧𓚨𓚩𓚪𓚫𓚬𓚭𓚮𓚯𓚰𓚱𓚲𓚳𓚴𓚵𓚶𓚷𓚸𓚹𓚺𓚻𓚼𓚽𓚾𓚿𓛀𓛁𓛂𓛃𓛄𓛅𓛆𓛇𓛈𓛉𓛊𓛋𓛌𓛍𓛎𓛏𓛐𓛑𓛒𓛓𓛔𓛕𓛖𓛗𓛘𓛙𓛚𓛛𓛜𓛝𓛞𓛟𓛠𓛡𓛢𓛣𓛤𓛥𓛦𓛧𓛨𓛩𓛪𓛫𓛬𓛭𓛮𓛯𓛰𓛱𓛲𓛳𓛴𓛵𓛶𓛷𓛸𓛹𓛺𓛻𓛼𓛽𓛾𓛿𓜀𓜁𓜂𓜃𓜄𓜅𓜆𓜇𓜈𓜉𓜊𓜋𓜌𓜍𓜎𓜏𓜐𓜑𓜒𓜓𓜔𓜕𓜖𓜗𓜘𓜙𓜚𓜛𓜜𓜝𓜞𓜟𓜠𓜡𓜢𓜣𓜤"
        ledes_text = self.ledes_builder.add_line_item(
            invoice_description=nonsense, line_item_description=nonsense
        ).build()

        result = self.parser.parse(ledes_text)
        self.assertIsNotNone(result)
        self.assertIn(nonsense, result.pretty())

    def test_can_parse_descriptions_with_semicolons(self):
        invoice_description_with_semicolon = "For services rendered; other things"
        line_item_description_with_semicolon = "Trademark Filing; 1234"
        ledes_text = self.ledes_builder.add_line_item(
            invoice_description=invoice_description_with_semicolon,
            line_item_description=line_item_description_with_semicolon,
        ).build()

        result = self.parser.parse(ledes_text)
        self.assertIsNotNone(result)
        self.assertIn("For services rendered; other things", result.pretty())
        self.assertIn("Trademark Filing; 1234", result.pretty())

    def test_can_parse_line_item_total_with_signs(self):
        ledes_text = (
            self.ledes_builder.add_line_item(
                line_item_adjustment_amount="+100.00", line_item_total="+100.00"
            )
            .add_line_item(
                line_item_adjustment_amount="-100.00", line_item_total="-100.00"
            )
            .build()
        )

        result = self.parser.parse(ledes_text)
        self.assertIsNotNone(result)
        self.assertIn("+100.00", result.pretty())
        self.assertIn("-100.00", result.pretty())

    def test_can_parse_valid_adjustment_amount_and_line_item_total(self):
        ledes_text = self.ledes_builder.add_line_item(
            exp_fee_inv_adj_type="IF",
            line_item_number_of_units="1.000",
            line_item_adjustment_amount="-117.000",
            line_item_total="-117.000",
        ).build()

        result = self.parser.parse(ledes_text)
        self.assertIsNotNone(result)
        self.assertIn("-117.000", result.pretty())

    def test_can_parse_timekeeper_name_with_dots(self):
        ledes_text = self.ledes_builder.add_line_item(
            timekeeper_name="Arnsley, Robert Sr."
        ).build()

        result = self.parser.parse(ledes_text)
        self.assertIsNotNone(result)
        self.assertIn("Arnsley, Robert Sr.", result.pretty())

    def test_can_parse_invoice_total_with_zero_to_four_decimals(self):
        amounts = ["1053", "1053.", "1053.0", "1053.00", "1053.000", "1053.0000"]
        for i, amount in enumerate(amounts):
            self.ledes_builder.add_line_item(
                invoice_number=str(i), invoice_total=amount
            )
        ledes_text = self.ledes_builder.build()

        result = self.parser.parse(ledes_text)
        self.assertIsNotNone(result)
        parsed_output = result.pretty()
        for amount in amounts:
            self.assertIn(amount, parsed_output)

    def test_parse_description_with_periods(self):
        ledes_text = (
            self.ledes_builder.add_line_item(
                invoice_description="U.S. Trademark Matters"
            )
            .add_line_item(line_item_description="U.S.-related things...")
            .build()
        )

        result = self.parser.parse(ledes_text)
        self.assertIsNotNone(result)
        self.assertIn("U.S. Trademark Matters", result.pretty())
        self.assertIn("U.S.-related things...", result.pretty())

    def test_parse_empty_text_raises_exception(self):
        data = ""
        with self.assertRaises(Exception):
            self.parser.parse(data)

    def test_parse_incorrect_format_raises_exception(self):
        data = """
NOT_THE_SPEC[]
INVOICE_DATE|INVOICE_NUMBER|CLIENT_ID|LAW_FIRM_MATTER_ID|INVOICE_TOTAL|BILLING_START_DATE|BILLING_END_DATE|INVOICE_DESCRIPTION|LINE_ITEM_NUMBER|EXP/FEE/INV_ADJ_TYPE|LINE_ITEM_NUMBER_OF_UNITS|LINE_ITEM_ADJUSTMENT_AMOUNT|LINE_ITEM_TOTAL|LINE_ITEM_DATE|LINE_ITEM_TASK_CODE|LINE_ITEM_EXPENSE_CODE|LINE_ITEM_ACTIVITY_CODE|TIMEKEEPER_ID|LINE_ITEM_DESCRIPTION|LAW_FIRM_ID|LINE_ITEM_UNIT_COST|TIMEKEEPER_NAME|TIMEKEEPER_CLASSIFICATION|CLIENT_MATTER_ID[]
19990225|96542|00711|0528|1684.45|19990101|19990131|For services rendered|1|F|2.00|-70|630|19990115|L510||A102|22547|Research Attorney's fees, Set off claim|24-6437381|350|Arnsley, Robert|PARTNR|423-987[]
"""
        with self.assertRaises(Exception):
            self.parser.parse(data)


if __name__ == "__main__":
    unittest.main()
