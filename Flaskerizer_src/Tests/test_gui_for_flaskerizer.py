import unittest
import os
from Flaskerizer_src.gui_for_flaskerizer import ChooseFilesGUI

class TestGUI(unittest.TestCase):

    def setUp(self):
        '''Instantiates an object 'test' from the ChoseFilesGUI class.
        '''
        self.test = ChooseFilesGUI(True)

    def test_values(self):
        """Gets the default values from the html,
        static and js string variables in the ChooseFilesGUI. Then
        sets new ones and tests to see if they are fully
        functional.
        """
        self.assertEqual(self.test.get_values(),
                         ["Select one HTML file from the template",
         "Select the template folder containing all the css, img, js folders",
         "Select one JavaScript (.js) file from the template JavaScript folder"])
        self.test.html_location.set("Html Location")
        self.test.static_location.set("Static Location")
        self.test.js_location.set("JS Location")
        self.assertEqual(self.test.get_values(),
                         ['Html Location', "Static Location",
         "JS Location"])

    def test_path(self):
        """Tests the path_to_folder function from ChooseFilesGUI
        gives it two files paths uses the function
        and compares it to this directory path.
        """
        self.this_directory = os.path.dirname(os.path.abspath(__file__))
        self.path_to_folder = self.test.path_to_folder
        self.assertEqual(self.path_to_folder(self.this_directory + "/gui_for_flaskerizer.py"), (self.this_directory))
        self.assertEqual(self.path_to_folder(self.this_directory + "/flaskerizer.py"), (self.this_directory))


if __name__ == '__main__':
    unittest.main()
