import unittest
from flaskerizer import Flaskerizer
import os


#ToDo look at https://github.com/selkind/text_analysis/tree/master/input_filtering/tests as example of class testing

class TestFlaskerizer(unittest.TestCase):
    def test_mkdir(self):
        test = Flaskerizer(directroy=r'C:\Users\vande060\Desktop\coding\projects\Flaskerizer\Folio')
        test.mkdir('static')
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), os.path.basename('static'))))

if __name__ == "__main__":
    unittest.main()