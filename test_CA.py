from datetime import datetime
import sys
from contextlib import redirect_stdout
import unittest
import CA

CONSOLE_OUTPUT = 1
WRITE_LOG = 0
LOG_FILE = "ca_unit_test_" + \
           str(datetime.now().strftime("%Y%m%d_%H%M%S")) + ".txt"


class TestCA(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def setUp(cls):
        pass

    @classmethod
    def tearDown(cls):
        print(datetime.now())

    def test_bin_to_dec(self):
        """
        Test Case #1
        Check to see if return type is int and correct value
        """
        expression = [1, 0, 0, 0]
        expression = expression[::-1]  # reverse ordinal value
        result = CA.bin_to_dec(expression)
        expected = 8
        self.assertTrue(type(result is int))
        self.assertEqual(result, expected)

        """
        Test Case #2
        Check to see if return type is int and correct value
        """
        expression = "0000"
        expression = expression[::-1]  # reverse ordinal value
        result = CA.bin_to_dec(expression)
        expected = 0
        self.assertTrue(type(result is int))
        self.assertEqual(result, expected)

        """
        Test Case #3
        Check for length
        """
        expression = "1111"
        expression = expression[::-1]  # reverse ordinal value
        result = CA.bin_to_dec(expression)
        expected = 15
        self.assertEquals(result, expected)

        """
        Test Case #4
        Check for non-integer values
        """
        result = "AAAA"
        self.assertRaises(ValueError, CA.bin_to_dec, result)

        """
        Test Case #5
        Check for non-valid types such as none
        """
        result = None
        self.assertRaises(TypeError, CA.bin_to_dec, result)

    def test_dec_to_bin(self):
        """
        Test Case #1
        Check return type
        """
        result = type(CA.dec_to_bin(8, 4))
        self.assertTrue(result is list)

        """
        Test Case #2
        Check for expected value
        Values are ordinal so they need to be reversed
        """
        result = CA.dec_to_bin(8, 4)
        expected = [1, 0, 0, 0]
        expected = expected[::-1]  # reversed
        self.assertEqual(result, expected)

        """
        Test Case #3
        Check for edge case
        """
        result = CA.dec_to_bin(0, 4)
        expected = [0, 0, 0, 0]
        expected = expected[::-1]  # reversed
        self.assertEqual(result, expected)

        """
        Test Case #3
        Check for edge case
        """
        result = CA.dec_to_bin(15, 4)
        expected = [1, 1, 1, 1]
        expected = expected[::-1]  # reversed
        self.assertEqual(result, expected)

    def test_make_rule_table(self):
        """
        Test Case #1
        Check return type
        """
        result = type(CA.make_rule_table(30, 1))
        self.assertTrue(result is list)

        """
        Test Case #2
        Check rule 30 for correct value
        """
        result = CA.make_rule_table(30, 1)
        expected = [0, 1, 1, 1, 1, 0, 0, 0]
        self.assertEqual(result, expected)

        """
        Test Case #3
        Check for correct length
        """
        result = CA.make_rule_table(30, 1)
        expected = 8
        result_len = len(result)
        self.assertEqual(result_len, expected)

        """
        Test Case #4
        Check for edge case
        """
        result = CA.make_rule_table(0, 1)
        expected = 8  # default bits are equal to 8
        result_len = len(result)
        self.assertEqual(result_len, expected)

    def test_make_config(self):
        """
        Test Case #1
        Check for correct return type
        """
        result = type(CA.make_config(30, 1))
        self.assertTrue(result is list)

        """
        Test Case #2
        Check for correct values
        """
        result = CA.make_config(30, 8)
        expected = [0, 1, 1, 1, 1, 0, 0, 0]
        self.assertEqual(result, expected)

        """
        Test Case #3
        Check for correct length
        """
        result = len(CA.make_config(30, 8))
        expected = 8
        self.assertEqual(result, expected)

        """
        Test Case #4
        Test edge case
        """
        result = CA.make_config(0, 8)
        expected = [0, 0, 0, 0, 0, 0, 0, 0]
        expected = expected[::-1]
        self.assertEqual(result, expected)

    def test_evolve_one_step(self):
        """
        Test Case #1
        Rule 30 evolved over 1 generation
        """
        rule_table = CA.make_rule_table(30, 1)
        rule_30 = CA.evolve_one_step(rule_table, [1, 0, 0, 0, 0, 0, 0, 0])
        expected = [1, 1, 0, 0, 0, 0, 0, 1]
        self.assertEqual(rule_30, expected)

        """
        Test Case #2
        Rule 90 evolved over 1 generation
        """
        rule_table = CA.make_rule_table(90, 1)
        rule_90 = CA.evolve_one_step(rule_table, [1, 0, 0, 0, 0, 0, 0, 0])
        expected = [0, 1, 0, 0, 0, 0, 0, 1]
        self.assertEqual(rule_90, expected)

        """
        Test Case #3
        Rule 184 evolved over 1 generation
        """
        rule_table = CA.make_rule_table(184, 1)
        rule_184 = CA.evolve_one_step(rule_table, [1, 0, 0, 0, 0, 0, 0, 0])
        expected = [0, 0, 0, 0, 0, 0, 0, 1]
        self.assertEqual(rule_184, expected)

        """
        Test Case #4
        Rule 102 evolved over 1 generation
        """
        rule_table = CA.make_rule_table(102, 1)
        rule_102 = CA.evolve_one_step(rule_table, [1, 0, 0, 0, 0, 0, 0, 0])
        expected = [1, 1, 0, 0, 0, 0, 0, 0]
        self.assertEqual(rule_102, expected)

        """
        Test Case #5
        Rule 222 evolved over 1 generation
        """
        rule_table = CA.make_rule_table(222, 1)
        rule_222 = CA.evolve_one_step(rule_table, [1, 0, 0, 0, 0, 0, 0, 0])
        expected = [1, 1, 0, 0, 0, 0, 0, 1]
        self.assertEqual(rule_222, expected)

    def test_evolve(self):
        """
        Test Case #1
        Rule 30 evolved over 1 radius of length 8 for 4 generations
        """
        rule_30 = CA.evolve(30, 1, 1, 8, 4)
        expected = [1, 0, 0, 1, 0, 0, 0, 0]
        self.assertEqual(rule_30[4], expected)

        """
        Test Case #2
        Rule 90 evolved over 1 radius of length 8 for 4 generations
        """
        rule_90 = CA.evolve(90, 1, 1, 8, 3)
        expected = [0, 1, 0, 1, 0, 1, 0, 1]
        self.assertEqual(rule_90[3], expected)

        """
        Test Case #3
        Rule 184 evolved over 1 radius of length 8 for 4 generations
        """
        rule_184 = CA.evolve(184, 1, 1, 8, 3)
        expected = [0, 0, 0, 0, 0, 1, 0, 0]
        self.assertEqual(rule_184[3], expected)

        """
        Test Case #4
        Rule 102 evolved over 1 radius of length 8 for 4 generations
        """
        rule_102 = CA.evolve(102, 1, 1, 8, 3)
        expected = [1, 1, 1, 1, 0, 0, 0, 0]
        self.assertEqual(rule_102[3], expected)

        """
        Test Case #5
        Rule 222 evolved over 1 radius of length 8 for 4 generations
        """
        rule_222 = CA.evolve(222, 1, 1, 8, 3)
        expected = [1, 1, 1, 1, 0, 1, 1, 1]
        self.assertEqual(rule_222[3], expected)

    def test_take_sequence(self):
        pass
        """
        Test Case #1
        """

        """
        Test Case #2
        """

        """
        Test Case #3
        """

        """
        Test Case #4
        """

        """
        Test Case #5
        """

    def test_generate_ca_sequence(self):
        """
        Test Case #1
        Check return type
        """
        result = type(CA.generate_ca_sequence(30, 1, 1, 8, 10))
        self.assertTrue(result is list)

        """
        Test Case #2
        Check for correct values
        """
        result = CA.generate_ca_sequence(30, 1, 1, 8, 10)
        expected = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1]
        self.assertEqual(result, expected)

        """
        Test Case #3
        Check for length
        """
        result = len(CA.generate_ca_sequence(30, 1, 1, 8, 1))
        expected = 2  # number generations + 1 (zero indexing)
        self.assertEqual(result, expected)

        """
        Test Case #4
        Check for edge case
        """
        result = len(CA.generate_ca_sequence(30, 1, 1, 8, 0, 1))
        expected = 1  # number of generations + 1 (zero indexing)
        self.assertEqual(result, expected)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestCA('test_bin_to_dec'))
    suite.addTest(TestCA('test_dec_to_bin'))
    suite.addTest(TestCA('test_make_rule_table'))
    suite.addTest(TestCA('test_make_config'))
    suite.addTest(TestCA('test_evolve_one_step'))
    suite.addTest(TestCA('test_evolve'))
    suite.addTest(TestCA('test_take_sequence'))
    suite.addTest(TestCA('test_generate_ca_sequence'))
    return suite


if __name__ == '__main__':

    # write to LOG_FILE
    if WRITE_LOG == 1:
        with open(LOG_FILE, 'w') as f:
            with redirect_stdout(f):
                runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=2)
                runner.run(suite())

    # write to console
    if CONSOLE_OUTPUT == 1:
        runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=2)
        runner.run(suite())
