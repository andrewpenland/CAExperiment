from datetime import datetime
import sys
from contextlib import redirect_stdout
import unittest
import CA

LOG_FILE = "ca_unit_test_" + \
           str(datetime.now().strftime("%Y%m%d_%H%M%S")) + ".txt"


class TestCA(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass
        #print(datetime.now())

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
        self.assertTrue(type(CA.bin_to_dec("1000") is int))
        self.assertEqual(CA.bin_to_dec("1000"), 8)

        """
        Test Case #2
        Check to see if return type is int and correct value
        """
        self.assertTrue(type(CA.bin_to_dec("0000") is int))
        self.assertEqual(CA.bin_to_dec("0000"), 0)

        """
        Test Case #3
        Check for range (4 bits)
        """
        self.assertTrue(0 <= CA.bin_to_dec("1111") <= 15)

        """
        Test Case #4
        Check for non-integer values
        """
        self.assertRaises(ValueError, CA.bin_to_dec, "AAAA")

        """
        Test Case #5
        Check for non-valid types such as none
        """
        self.assertRaises(TypeError, CA.bin_to_dec, None)

        """
        Test Case #6
        Check for valid block size
        """
        self.assertIsNot(Exception, CA.bin_to_dec("1111"))

    def test_dec_to_bin(self):
        # check to see if we return a list
        self.assertTrue(type(CA.dec_to_bin(8, 4)) is list)
        # check to see if list contains correct values
        self.assertEqual(CA.dec_to_bin(8, 4), [1, 0, 0, 0])

    def test_make_rule_table(self):
        # check return type
        self.assertTrue(type(CA.make_rule_table(30, 1)) is list)
        # test rule 30
        self.assertEqual(CA.make_rule_table(30, 1), [0, 1, 1, 1, 1, 0, 0, 0])

    def test_make_config(self):
        pass

    def test_config_density(self):
        pass

    def test_evolve_one_step(self):
        pass

    def test_evolve(self):
        pass
        # print(CA.make_rule_table(30, 1))
        # state = [0, 0, 1, 0, 1, 1]
        # new_state = CA.evolve(30, 1, 1, 1, 1)
        # self.assertEqual(new_state, [1, 1, 1, 0, 0, 1])

    def test_random_initial_config(self):
        pass

    def test_random_initial_ensemble(self):
        pass

    def test_random_rule_table(self):
        pass

    def test_take_sequence(self):
        pass

    def test_generate_ca_sequence(self):
        pass

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestCA('test_bin_to_dec'))
    suite.addTest(TestCA('test_dec_to_bin'))
    suite.addTest(TestCA('test_make_rule_table'))
    suite.addTest(TestCA('test_make_config'))
    suite.addTest(TestCA('test_config_density'))
    suite.addTest(TestCA('test_evolve_one_step'))
    suite.addTest(TestCA('test_evolve'))
    suite.addTest(TestCA('test_random_initial_config'))
    suite.addTest(TestCA('test_random_initial_ensemble'))
    suite.addTest(TestCA('test_random_rule_table'))
    suite.addTest(TestCA('test_take_sequence'))
    suite.addTest(TestCA('test_generate_ca_sequence'))
    return suite


if __name__ == '__main__':
    with open(LOG_FILE, 'w') as f:
        with redirect_stdout(f):
            runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=2)
            runner.run(suite())
