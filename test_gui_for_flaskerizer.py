import unittest
from gui_for_flaskerizer import ChooseFilesGUI

class TestGUI(unittest.TestCase):
    def test_values(self):
        '''Test to get the default values, change and get again other values.
        '''
        self.testclass = ChooseFilesGUI(True)
        self.assertEqual(self.testclass.get_values(),
         ["Select the main html file, usually a index.html file",
          "The folder with images, .css, etc. If separated select the main folder",
         "Select the a .js file, one in the js folder if there is one"])
        self.testclass.html_location.set("Html Location")
        self.testclass.static_location.set("Static Location")
        self.testclass.js_location.set("JS Location")
        self.assertEqual(self.testclass.get_values(),
         ['Html Location', "Static Location",
         "JS Location"])


if __name__ == '__main__':
    unittest.main()