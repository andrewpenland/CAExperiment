import unittest
import CA


class TestCA(unittest.TestCase):

    def tearDown(self):
        pass

    def setUp(self):
        pass

    def test_bin_to_dec(self):
        # check to see if we return an integer
        self.assertTrue(type(CA.bin_to_dec("1000") is int))
        # check to see if value is correct
        self.assertEqual(CA.bin_to_dec("1000"), 8)

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
        print(CA.make_rule_table(30, 1))
        # state = [0, 0, 1, 0, 1, 1]
        # new_state = CA.evolve(30, 1, 1, 1, 1)
        # self.assertEqual(new_state, [1, 1, 1, 0, 0, 1])


if __name__ == '__main__':
    unittest.main()
