import unittest
from flaskerizer.flaskerizer_src.status_code_to_word import status_code_to_word


class TestStatusCode(unittest.TestCase):
    def test_status_code_to_word(self):
        '''Test the function against some dummy values and also test that the function returns a string
		'''
        self.assertEqual(status_code_to_word(9753160248), 'nine_seven_five_three_one_six_zero_two_four_eight')
        self.assertEqual((status_code_to_word(505)), 'five_zero_five')
        self.assertEqual((status_code_to_word(417)), 'four_one_seven')
        self.assertIsInstance(status_code_to_word('404'), str)

if __name__ == '__main__':
    unittest.main()