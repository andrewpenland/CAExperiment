import unittest
import CA

LOG_FILE = "ca_unit_test.txt"


class TestCA(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

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

    def test_evolve(self):
        pass
        # print(CA.make_rule_table(30, 1))
        # state = [0, 0, 1, 0, 1, 1]
        # new_state = CA.evolve(30, 1, 1, 1, 1)
        # self.assertEqual(new_state, [1, 1, 1, 0, 0, 1])


if __name__ == '__main__':
    # log file to write
    log_file = LOG_FILE
    # set logging verbosity
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCA)
    unittest.TextTestRunner(verbosity=2).run(suite)
    # write log file using context manager
    with open(log_file, "w") as f:
        runner = unittest.TextTestRunner(f)
        unittest.main(testRunner=runner)
    # main
    unittest.main()
