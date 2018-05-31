import unittest
from gui_for_flaskerizer import ChooseFilesGUI

class TestGUI(unittest.TestCase):
    def test_get_functions(self):
        '''Test to get the default values, change and get again.
        '''
        self.testclass = ChooseFilesGUI(True)
        self.assertEqual(self.testclass.get_values(),
         ['The folder with .html files', "The folder with images, .css, etc",
         "The folder with the .js files"])
        self.testclass.html_location.set("Html Location")
        self.testclass.static_location.set("Static Location")
        self.testclass.js_location.set("JS Location")
        self.assertEqual(self.testclass.get_values(),
         ['Html Location', "Static Location",
         "JS Location"])


if __name__ == '__main__':
    unittest.main()